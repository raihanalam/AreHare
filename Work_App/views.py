from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from Wallet_App.models import PendingPayment, Wallet
from Wallet_App.views import payment_complete, payment_confirm, wallet

from Work_App.models import Offer, Order, RunningWork, CompleteWork
from .forms import OrderForm, RunningWorkForm, WorkFileForm, ReportForm, NewOfferForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from notifications.signals import notify
from django.db.models import Q
# from django.contrib.auth import get_user_model
# User = get_user_model()

# from django.contrib.auth.models import User
from Account_App.models import User

# Create your views here.
@login_required
def get_work_data(request):
     f_user = request.GET.get('f_user')
     c_user = request.user
     recent_offer = Offer.objects.filter(customer=c_user, freelancer=f_user, status='Pending')
     recent_order = Order.objects.filter(customer=f_user, freelancer=c_user, payment_status='Pending', status='Placed')
     return JsonResponse({'offer_data': list(recent_offer.values()), 'order_data': list(recent_order.values())})


@login_required
def send_offer(request, receiver):
     
     user = User.objects.get(id=receiver)
     if request.method == "POST":
          new_offer_form = NewOfferForm(request.POST)
               
          if new_offer_form.is_valid():
               offer = new_offer_form.save(commit=False)
               offer.freelancer = request.user 
               offer.customer = user
               offer.save()

               notify.send(request.user, recipient = offer.customer, verb=f"{offer.freelancer.username} send you a offer.")
               messages.success(request,'Your offer has been send.')

     return HttpResponseRedirect(reverse('Main_App:all_hires'))

     


@login_required
def cancel_order(request, order_id):
     order = Order.objects.get(id=order_id)
     if order.status == 'Placed':
          if order.freelancer == request.user or order.customer == request.user:
               pending_payment = PendingPayment.objects.get(order_id=order)
               pending_payment.delete()
               order.status = 'Canceled'
               order.save()
               messages.warning(request, 'Your order is canceled.')
          else:
               messages.warning(request, 'You are not right user to cancel this.')
     else:
          messages.warning(request, 'This order cancelation is not possible.')

     
     return HttpResponseRedirect(reverse('Wallet_App:wallet_page'))




@login_required
def place_order(request,pk):
     c_user = request.user

     if request.method == 'POST' and c_user.user_profile.role == 'customer':
          order_form = OrderForm(request.POST)
          wallet = Wallet.objects.get(user = request.user)
          pendings = PendingPayment.objects.filter(user_id=request.user)

          total_pending = 0
          for p in pendings:
               if p.success == False and p.confirmation==True:
                    total_pending += p.amount

          if order_form.is_valid():
               offer = Offer.objects.get(pk=pk)
    
               try:
                    new_order = Order.objects.get(offer_id=offer)
                    data = order_form.cleaned_data
                    new_order.instruction = data['instruction']
                    new_order.amount=data['amount']
                    new_order.save()
               except:
                    new_order = order_form.save(commit=False)
                    new_order.offer_id = offer
                    new_order.customer = request.user
                    new_order.freelancer = offer.freelancer
                    new_order.save()

               if wallet.balance >= new_order.amount:

                    if  (wallet.balance - total_pending) >= new_order.amount: 
                         
                         messages.success(request, 'Your order is ready to place! Please confirm payment to send this order to freelancer.')
                         # notify.send(request.user, recipient = new_order.freelancer, verb=f"{new_order.freelancer.username} send you a order.")
                         return HttpResponseRedirect(reverse('Wallet_App:payment_checkout',  kwargs={'order_id': new_order.id}))
                    else:
                         messages.warning(request, 'You have some pending payments which will cutoff for running order, Please deposit some amount.')          
               else:
                    messages.warning(request, 'Your order is not possible, your balance is low.')

     return HttpResponseRedirect(reverse('Wallet_App:wallet_page'))

@login_required
def start_work(request,pk):
     start_work = RunningWorkForm()
     c_user = request.user
     order = Order.objects.get(pk=pk)

     if request.method == 'POST' and c_user.user_profile.role == 'freelancer':
          start_work = RunningWorkForm(request.POST)
          if start_work.is_valid():
               
               if order.status == 'Placed':
                    run_work = start_work.save(commit=False)
                    if run_work.running == True:
                         run_work.order_id = order
                         run_work.customer = order.customer
                         run_work.freelancer = c_user
                         run_work.ruuning = True
                         run_work.work_track = 0
                         order.status = 'Running'
                         run_work.save()
                         order.save()
                         notify.send(request.user, recipient = order.customer, verb=f"{request.user.username} just started his work.")
                         messages.success(request,'Congratulations! this order is just started.')
                    else:
                         messages.warning(request, 'Please check the box! and start work again please. ')
                         room = str(order.freelancer.username)+'_'+ str(order.customer.username)
                         return HttpResponseRedirect(reverse('Message_App:room', kwargs={'room_name':room}))

                    return HttpResponseRedirect(reverse('Work_App:running_work', kwargs={'order_id': order.id}))
               else:
                    messages.warning(request,'This order is already running or completed or canceled.')
               
          return HttpResponseRedirect(reverse('Work_App:all_orders'))

@login_required
def running_work(request, order_id):
     
     user = request.user
     file_form = WorkFileForm()
     report_form = ReportForm()


     running_order = Order.objects.get(id = order_id)
     running_work = RunningWork.objects.get(order_id = running_order)
  
     running_offer = Offer.objects.get(id = running_order.offer_id.id)


     if user.id == running_work.freelancer.id or user.id == running_work.customer.id:
          return render(request, 'running_work.html', context={'report_form': report_form,'file_form': file_form,'running_work':running_work, 'running_order': running_order, 'running_offer': running_offer })
     else:
          messages.warning(request,'You are not able to see this')
          return HttpResponseRedirect(reverse('Work_App:all_orders'))


     
@login_required
def push(request, work_id):
     running_work = RunningWork.objects.get(id=work_id)
     
     if running_work.freelancer == request.user:
          if running_work.work_track < 100:
               running_work.work_track += 10
               running_work.save()
          elif running_work.work_track >= 100:
               messages.success(request, 'Your tracker is already in success state.')
     

     return HttpResponseRedirect(reverse('Work_App:running_work', kwargs={'order_id':running_work.order_id.pk}))

          

@login_required
def pop(request, work_id):
     running_work = RunningWork.objects.get(id=work_id)
     
     if running_work.freelancer == request.user:
          if running_work.work_track > 0:
               running_work.work_track -= 10
               running_work.save()

          else:
               messages.warning(request, 'Your tracker is already in initial state.')

     return HttpResponseRedirect(reverse('Work_App:running_work', kwargs={'order_id':running_work.order_id.pk}))


@login_required
def send_file(request, work_id):

     try:
          work = RunningWork.objects.get(Q(id=work_id), Q(freelancer=request.user) | Q(customer=request.user))

          if work:
               if request.method == 'POST':
                    # data = request.POST.get("title", "")

                    data_form = WorkFileForm(request.POST, request.FILES)
                    if data_form.is_valid():
                         file_form = data_form.save(commit=False)
                         # file_form.file = data_form.cleaned_data['file']
                         file_form.file_name = file_form.file
                         file_form.work_id = work
                         file_form.user = request.user
                         file_form.save()
                         return HttpResponseRedirect(reverse('Work_App:running_work', kwargs={'order_id':work.order_id.pk}))
     except:
          messages.error(request, 'No work id exist.')

     return HttpResponseRedirect(reverse('Work_App:all_orders'))

     

@login_required       
def all_order(request):
     c_user = request.user
     run_form = RunningWorkForm()

     if c_user.user_profile.role == 'freelancer':
          all_order = Order.objects.filter(freelancer=c_user).exclude(status='Created')

     elif c_user.user_profile.role == 'customer':
          all_order = Order.objects.filter(customer=c_user)

     return render(request, 'all_order.html', context={'run_form':run_form,'all_order':all_order})


@login_required       
def complete_work(request, pk):
     user = request.user
     flag=False

     running_work = RunningWork.objects.get(pk=pk)
     order = Order.objects.get(id = running_work.order_id.id )

     try:
          check_complete = CompleteWork.objects.get(work_id=running_work)
          if check_complete:
               flag=True
     except:
          pass

     if user.id == running_work.freelancer.id:
               if flag == False:
                    complete_work = CompleteWork(order_id = running_work.order_id, work_id = running_work, freelancer=user, customer=running_work.customer, freelancer_confirmation = True)
                    complete_work.save()    
                    messages.info(request, 'Your work confirmation is send, wait for customer confirmation.')
                    #Notification will go from here.
               else:
                     messages.info(request, 'You dont have any running work like that.')

     elif user.id == running_work.customer.id:
          complete_work = CompleteWork.objects.get(work_id = running_work.id)
          complete_work.customer_confirmation = True
          complete_work.customer = user

          if complete_work.freelancer_confirmation == True:
               complete_work.completed = True
               running_work.completed = True
               running_work.running = False
               complete_work.save()
               running_work.save()
               order.status = 'Completed'
               order.save()
               return HttpResponseRedirect(reverse('Wallet_App:complete_payment', kwargs={'order_id':  order.id}))
          else:
               messages.error(request, 'Error here!')


     return HttpResponseRedirect(reverse('Work_App:running_work', kwargs={'order_id': order.id}))

@login_required
def all_running_orders(request):
     if request.user.user_profile.role == 'customer':
          running_orders = Order.objects.filter(customer=request.user, status='Running', payment_status='Pending')

     elif request.user.user_profile.role == 'freelancer':
          running_orders = Order.objects.filter(freelancer=request.user, status='Running', payment_status='Pending')


     return render(request, 'all_running_orders.html', context={'all_running_orders':running_orders})

@login_required
def all_succesfull_orders(request):
     if request.user.user_profile.role == 'customer':
          successfull_orders = Order.objects.filter(customer=request.user, status='Completed', payment_status='Succeed')
     elif request.user.user_profile.role == 'freelancer':
          successfull_orders = Order.objects.filter(freelancer=request.user, status='Completed',  payment_status='Succeed')


     return render(request, 'successfull_orders.html', context={'all_successfull_orders':successfull_orders})


@login_required
def give_report(request, work_id):
     form = ReportForm()
     work = RunningWork.objects.get(id=work_id)

     if request.method == 'POST':
          form = ReportForm(request.POST)

          if form.is_valid():
               report = form.save(commit=False)
               report.work_id = work
               report.user = request.user
               report.save()
               messages.info(request, 'Your report has been send. Please wait for verification.')

     return HttpResponseRedirect(reverse('Work_App:running_work', kwargs={'order_id': work.order_id.id}))



@login_required
def all_offers(request):

     offers = {}
     order_form = OrderForm()

     if request.user.user_profile.role == 'customer':
          offers = Offer.objects.filter(customer=request.user)

     
     return render(request, 'all_offers.html', context={'order_form':order_form,'all_offers':offers})


@login_required
def recent_oders(request):

     orders = {}
     startwork_form = RunningWorkForm()

     if request.user.user_profile.role == 'freelancer':
          orders = Order.objects.filter(freelancer=request.user, status='Placed', payment_status='Pending')

     
     return render(request, 'recent_orders.html', context={'run_form':startwork_form,'recent_orders':orders})

