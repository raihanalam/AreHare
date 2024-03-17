from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView, TemplateView, ListView

from django.contrib.auth.decorators import login_required #Used in function based views
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Category, PortImageGallery, Post,Port,Bid,Hire, ReviewRating, SavedPort
from Account_App.models import UserProfile
from django.contrib.auth.models import User
from .forms import BidForm, HireForm, PortForm, ReviewForm, PortEditForm, PostForm, PostEditForm, PublicPostForm
from Work_App.forms import NewOfferForm
import uuid
from django import forms
from django.contrib import messages
from notifications.signals import notify
from django.db.models import Avg

#Getting custom base User model
from django.contrib.auth import get_user_model
User = get_user_model()

#For Pagination Ajax
from django.core import serializers
from django.http import JsonResponse

from Account_App.decorators import user_is_verified


#Django Pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
@login_required
def home(request):
     this_user = request.user
     category = Category.objects.all()
     if this_user.user_profile.role == 'freelancer':
          posts_list=Post.objects.filter(active=True)
          page = request.GET.get('page', 1)
          paginator = Paginator(posts_list, 20)

          try:
               posts = paginator.page(page)
          except PageNotAnInteger:
               posts = paginator.page(1)
          except EmptyPage:
               posts = paginator.page(paginator.num_pages)

          # Pagintion
          # paginator=Paginator(posts,2)
          # page_number=request.GET.get('page')
          # posts_obj=paginator.get_page(page_number)
     
         
          return render(request,'home.html',{'posts':posts, 'categories_list': category})
          
     elif this_user.user_profile.role == 'customer':
          ports_list=Port.objects.filter(active=True).order_by('-rating')
          page = request.GET.get('page', 1)
          paginator = Paginator(ports_list, 20)

          try:
               ports = paginator.page(page)
          except PageNotAnInteger:
               ports = paginator.page(1)
          except EmptyPage:
               ports = paginator.page(paginator.num_pages)
               
          return render(request, 'home.html', context={'ports': ports,  'categories_list': category})
     else:
          return render(request, 'home.html', context={})


@login_required
def load_more(request):
     if request.user.user_profile.role == 'freelancer':
          offset=int(request.POST['offset'])
          limit=2
          posts=Post.objects.filter(active=True)[offset:limit+offset]
          totalData=Post.objects.filter(active=True).count()
          data={}
          posts_json=serializers.serialize('json',posts)
          print(totalData,posts_json, posts)
          return JsonResponse(data={
               'posts':posts_json,
               'totalResult':totalData
          })

     elif request.user.user_profile.role == 'customer':
          offset=int(request.POST['offset'])
          limit=2
          ports=Port.objects.filter(active=True)[offset:limit+offset]
          totalData=Port.objects.filter(active=True).count()
          data={}
          ports_json=serializers.serialize('json',ports)
          print(totalData,ports_json, ports)
          return JsonResponse(data={
               'ports':ports_json,
               'totalResult':totalData
          })   



#######################
#Customer Related Code#
#######################

class CreatePost(LoginRequiredMixin, CreateView):
     model = Post
     template_name = 'create_post.html'

     form_class = PostForm
     # fields = ('post_category','post_title','required_skills','post_description','budget_amount','post_image','keywords')
     # widgets = {
     #      'post_title': forms.TextInput(attrs={'placeholder':'Title'}),
     # }

     def form_valid(self,form):
          post_obj = form.save(commit=False)
          post_obj.post_author = self.request.user 
          title = post_obj.post_title
          post_obj.post_image = form.cleaned_data['post_image']
          post_obj.slug = title.replace(" ","-") + "-" + str(uuid.uuid4())
          post_obj.active = True
          post_obj.save()

          # return HttpResponseRedirect(reverse_lazy('index'))
          messages.success(self.request,'Your job posted.')
          return HttpResponseRedirect('')


@login_required
def post_details(request, slug):
     post = Post.objects.get(slug=slug)
     ports = Port.objects.filter(port_author = request.user, active=True)

     

     user_profile = UserProfile.objects.get(user=post.post_author)
     about_user = User.objects.get(username=post.post_author.username)

     bid_form = BidForm()
     
     already_bade = Bid.objects.filter(post = post, user = request.user)
     if already_bade:
          bidden = True
     else:
          bidden = False

     if request.method == 'POST':
          bid_form = BidForm(request.POST)
          if bid_form.is_valid():
               bid = bid_form.save(commit=False)
               bid.user = request.user
               port_pk= request.POST.get('port')
               port = Port.objects.get(port_author=request.user, pk=port_pk)
               bid.port = port
               bid.post = post
               bid.save()
               return HttpResponseRedirect(reverse('Main_App:post_details', kwargs={'slug':slug}))
     else:
          return render(request,'post_details.html',context={'ports':ports, 'post':post,'uProfile':user_profile, 'aUser':about_user,'bid_form':bid_form, 'bidden':bidden})

@login_required
def unbid(request,pk):
     post = Post.objects.get(pk=pk)
     user = request.user
     already_bade = Bid.objects.filter(post=post,user=user)
     already_bade.delete()
     return HttpResponseRedirect(reverse('Main_App:post_details', kwargs={'slug':post.slug}))


@login_required
def review_bid(request, pk):
     bid = Bid.objects.get(pk=pk)
     bid.status = 'reviewed'
     bid.save()
    
     # Get the referer (previous) page from request.META
     referer = request.META.get('HTTP_REFERER', '/')
    
     return redirect(referer)

@login_required
def reject_bid(request,pk):
     bid = Bid.objects.get(pk=pk)
     bid.status = 'rejected'
     bid.save()
     return HttpResponseRedirect('/')



class MyPosts(LoginRequiredMixin,TemplateView):
     template_name = 'my_posts.html'

class UpdatePost(LoginRequiredMixin, UpdateView):

     model = Post

     # fields = ('post_title','post_description','post_image',)
     form_class = PostEditForm
     template_name = 'edit_post.html'


     def get_success_url(self,**kwargs):
          return reverse_lazy('Main_App:post_details', kwargs={'slug':self.object.slug})


@login_required
def all_bids(request):
     data  = Post.objects.filter(post_author=request.user, active=True)
     id_set = []
     for d in data:
          id_set.append(d.id)

     bid = Bid.objects.filter(post__in=id_set)
     return render(request,'all_bids.html',context={'all_bids': bid})

def active_post_list(request):
     data  = Post.objects.filter(post_author=request.user, active=True)

     return render(request, 'active_post.html', context={'type':'Active','all_post':data})

def deactivated_post_list(request):
     data  = Post.objects.filter(post_author=request.user, active=False)

     return render(request, 'active_post.html', context={'type':'Inactive', 'all_post':data})

@login_required
def deactivate_post(request, pk):

     post = Post.objects.get(id=pk, post_author=request.user)

     if post.post_author == request.user and request.user.user_profile.role == 'customer':
          post.active = False
          post.save()
     
     return HttpResponseRedirect(reverse_lazy('Main_App:deactivated_post_list'))
     
@login_required
def activate_post(request, pk):

     post = Post.objects.get(id=pk, post_author=request.user)

     if post.post_author == request.user and request.user.user_profile.role == 'customer':
          post.active = True
          post.save()
     
     return HttpResponseRedirect(reverse_lazy('Main_App:active_post_list'))



#Deleting Post
@login_required
def delete_post(request, pk):

     post = Post.objects.get(id=pk, post_author=request.user)

     if post.post_author == request.user and request.user.user_profile.role == 'customer':
          post.delete()
          messages.error(request, 'Your post has been deleted.')
     
     return HttpResponseRedirect(reverse_lazy('Main_App:my_posts'))

#Submitting review to user profile
def submit_review(request, freelancer):
#     url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
               data = ReviewRating()
               data.rating = form.cleaned_data['rating']
               data.review = form.cleaned_data['review']
               f_u = User.objects.get(id=freelancer)
               data.freelancer = f_u
               data.customer_id = request.user.id
               data.save()
               messages.success(request, 'Thank you! Your review has been submitted.')
               return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




#########################
#Freelancer Related Code
#########################


class CreatePort(LoginRequiredMixin, CreateView):
     model = Port
     # port_title = forms.CharField(required=True,label="",widget=forms.TextInput(attrs={'placeholder':'Title', 'style':'margin-bottom:10px; padding:8px; width: 70%;', 'class': 'form-control'}))

     template_name = 'create_port.html'
     form_class = PortForm

     def form_valid(self,form):
          port_obj = form.save(commit=False)
          port_obj.port_author = self.request.user 
          title = port_obj.port_title
          port_obj.port_image = form.cleaned_data['port_image']
          port_obj.slug = title.replace(" ","-") + "-" + str(uuid.uuid4())
          port_obj.active = True
          port_obj.save()

          return HttpResponseRedirect(reverse('Main_App:edit_port', kwargs={'pk':port_obj.id}))


@login_required
def port_bulk_image_upload(request, port_id):

     port = Port.objects.get(id=port_id)

     if port.port_author == request.user:

          if request.method == 'POST':
               file=request.FILES.get('image_file')

               gallery = PortImageGallery()

               gallery.port = port
               gallery.image = file
               gallery.save()
               # return HttpResponseRedirect('')

     return HttpResponseRedirect(reverse('Main_App:edit_port', kwargs={'pk':port.id}))
     


# @login_required
def port_details(request, slug):

     port = Port.objects.get(slug=slug)
     ratings = port.port_author.freelancer_profile_ratings.all()



     rating_average = ratings.aggregate(Avg('rating'))['rating__avg'] if ratings.aggregate(Avg('rating'))['rating__avg'] else 0
     rating_count = ratings.count() if ratings.count() else 0

     star_counts = [ratings.filter(rating=i).count() for i in range(1, 6)]
     star_counts.reverse()
     ratings_points = [1,2,3,4,5]
     width = []
     for val in star_counts:
          width.append(val*5)

     combined_list = zip([5,4,3,2,1], star_counts, width)



     context = {'port': port, 'rating_count': str(rating_count), 'rating_average': str(rating_average), 'star_counts': combined_list, 'ratings_points': ratings_points}

     try:
          posts = {}
          posts = Post.objects.filter(post_author = request.user, active=True)

          user_profile = UserProfile.objects.get(user=port.port_author)
          about_user = User.objects.get(username=port.port_author.username)
          port_image_gallery = PortImageGallery.objects.filter(port=port.id)

          hire_form = HireForm()
          already_hired = Hire.objects.filter(port = port, user = request.user)
          reviews = ReviewRating.objects.filter(freelancer=about_user)

          if already_hired:
               hired = True
          else:
               hired = False

          if request.method == 'POST':
               hire_form = HireForm(request.POST)
               if hire_form.is_valid():
                    hire = hire_form.save(commit=False)
                    hire.user = request.user
                    hire.port = port
                    try:
                         post_pk= request.POST.get('post')
                         post = Post.objects.get(post_author=request.user, pk=post_pk)
                         hire.post = post
                         
                    except:
                         pass
                    hire.save()
                    notify.send(request.user, recipient = port.port_author, verb=f"{request.user.username} send you a hire request.")
                    messages.success(request,'Your hire request has been send.')

                    return HttpResponseRedirect(reverse('Main_App:port_details', kwargs={'slug':slug}))
          else:
               context.update({
                    'posts':posts,
                    'uProfile':user_profile,
                    'aUser':about_user,
                    'hire_form':hire_form,
                    'hired':hired, 
                    'reviews':reviews,
                    'port_image_gallery':port_image_gallery,
               })
     except:
          pass
     
     return render(request,'port_details.html',context)
          
@login_required
def cancel_hire_rquest(request,pk):
     port = Port.objects.get(pk=pk)
     user = request.user
     already_hired = Hire.objects.filter(port=port,user=user)
     already_hired.delete()
     return HttpResponseRedirect(reverse('Main_App:port_details', kwargs={'slug':port.slug}))


@login_required
def all_hires_requests(request):
     offer_form = NewOfferForm()
     data  = Port.objects.filter(port_author=request.user, active=True)
     id_set = []
     for d in data:
          id_set.append(d.id)

     hires = Hire.objects.filter(port__in=id_set)
     return render(request,'all_hires.html',context={'offer_form': offer_form,'all_hires': hires})

class MyPorts(LoginRequiredMixin,TemplateView):

     template_name = 'my_ports.html'

class UpdatePort(LoginRequiredMixin, UpdateView):

     model = Port

     # fields = ('port_title','expert','keywords','port_description','port_image','rate_amount')
     template_name = 'edit_port.html'
     form_class = PortEditForm

     def get_success_url(self,**kwargs):
          return reverse_lazy('Main_App:port_details', kwargs={'slug':self.object.slug})


def active_port_list(request):
     data  = Port.objects.filter(port_author=request.user, active=True)

     return render(request, 'active_port.html', context={'type':'Active','all_port':data})

def deactivated_port_list(request):
     data  = Port.objects.filter(port_author=request.user, active=False)

     return render(request, 'active_port.html', context={'type':'Deactivated', 'all_port':data})

@login_required
def deactivate_port(request, pk):

     port = Port.objects.get(id=pk, port_author=request.user)

     if port.port_author == request.user and request.user.user_profile.role == 'freelancer':
          port.active = False
          port.save()
     
     return HttpResponseRedirect(reverse_lazy('Main_App:deactivated_port_list'))
     
@login_required
def activate_port(request, pk):

     port = Port.objects.get(id=pk, port_author=request.user)

     if port.port_author == request.user and request.user.user_profile.role == 'freelancer':
          port.active = True
          port.save()
     
     return HttpResponseRedirect(reverse_lazy('Main_App:active_port_list'))



#Deleting Post
@login_required
def delete_port(request, pk):

     port = Port.objects.get(id=pk, port_author=request.user)

     if port.port_author == request.user and request.user.user_profile.role == 'freelancer':
          port.delete()
     
     return HttpResponseRedirect(reverse_lazy('Main_App:my_ports'))
     

@login_required
def quick_quize(request):
     return render(request,'quick_quize.html')



@login_required
def save_port(request, port_id):

     port = Port.objects.get(id=port_id)
     new_save = SavedPort(port_id=port,user=request.user)
     return HttpResponseRedirect('')


#Deleting port bulk image
@login_required
def delete_port_gallery_image(request,port_id, img_id):

     img = PortImageGallery.objects.get(id=img_id)

     if  request.user.user_profile.role == 'freelancer':
          img.delete()

     messages.success(request, 'Image removed from port gallery.')
     return HttpResponseRedirect(reverse('Main_App:edit_port', kwargs={'pk':port_id}))
     
     # return HttpResponseRedirect(reverse_lazy('Main_App:my_ports'))

def public_post(request):
     if request.method == 'POST':
          form = PublicPostForm(request.POST, request.FILES)
          if form.is_valid():
               form.save()
               messages.success(request, 'Thank you for submitting your idea. Our team of expertise will analyze your project. We will contact you soon.')
          else:
            # Form is not valid, show errors
            messages.error(request, 'There was an error in your submission. Please correct the errors below.')
     else:
        form = PublicPostForm()
     return HttpResponseRedirect('/')