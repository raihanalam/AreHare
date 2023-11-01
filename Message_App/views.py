
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from Wallet_App.views import payment_confirm

from Work_App.views import running_work
from .models import Chat, ChatRoom
from django.urls import reverse
from django.contrib.auth.models import User
from Work_App.forms import *
from Work_App.models import Offer
from notifications.signals import notify

from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.
class Room(LoginRequiredMixin, View):
     def get(self, request, room_name):
          c_user = request.user
          f_user = ''
          
          offer_form = NewOfferForm()
          order_form = OrderForm()
          run_form =  RunningWorkForm()
          
          
          room = ChatRoom.objects.filter(name=room_name,users__username=c_user.username).first()
          for user in room.users.all():
               if user.id != c_user.id:
                    f_user = user

         
          recent_offer = {}
          recent_order = {}
          running_work = {}
 
          try:
               if request.user.user_profile.role == 'customer':
                    recent_offer = Offer.objects.filter(customer=c_user, freelancer=f_user, status='Pending')
                    running_work = RunningWork.objects.filter(customer=c_user, freelancer=f_user, completed=False)
               elif request.user.user_profile.role == 'freelancer':
                    recent_order = Order.objects.filter(customer=f_user, freelancer=c_user, status='Placed' )
                    running_work = RunningWork.objects.filter(freelancer=c_user, customer=f_user, completed=False)
          except:
               pass


          chats = []

          if room:
               chats = Chat.objects.filter(room=room)
               
               return render(request, 'chatroom.html', context={'room_name':room_name, 'current_room':room, 'chats':chats, 'offer_form': offer_form, 'recent_offer':recent_offer, 'order_form':order_form, 'recent_order': recent_order, 'run_form': run_form, 'running_work':running_work,'r_user':request.user, 'f_user':f_user })
          else:
               #room = ChatRoom(name=room_name)
               #room.save()
               messages.warning(request,f"You are not added to {room_name} chat!")
               return HttpResponseRedirect(reverse('Message_App:inbox'))

          #return render(request, 'chatroom.html', context={'room_name':room_name, 'chats':chats})
     def post(self, request, room_name):
          c_user = request.user
          
          room = ChatRoom.objects.filter(name=room_name,users__username=c_user.username).first()
          
          if request.method == "POST":
               new_offer_form = NewOfferForm(request.POST)
               
               if new_offer_form.is_valid():
                    offer = new_offer_form.save(commit=False)
                    offer.freelancer = request.user
                    for user in room.users.all():
                         if user.id != c_user.id:
                              offer.customer = user
                    offer.save()
                    notify.send(request.user, recipient = offer.customer, verb=f"{offer.freelancer.username} send you a offer.")
                    messages.success(request,'Your offer has been send.')
          return HttpResponseRedirect(reverse('Message_App:room', kwargs={'room_name':room_name}))



class Inbox(LoginRequiredMixin, View):
     def get(self, request):
          c_user = request.user
          my_rooms = ChatRoom.objects.filter(users__id=c_user.id)

          return render(request, 'inbox.html', context={'my_rooms':my_rooms})
  
@login_required
def join_chat(request,f_username):
     c_user = request.user
     f_user = User.objects.get(email = f_username)
     room_name = f_user.username +"_"+ c_user.username
     
     room = ChatRoom.objects.filter(name=room_name,users__username=c_user.username).first()
     
     if room:
          return HttpResponseRedirect(reverse('Message_App:room',kwargs={'room_name': room_name}))
     else:
          new_chat = ChatRoom(name=room_name)
          new_chat.save()
          new_chat.connect_user(c_user)
          new_chat.connect_user(f_user.pk)
     return HttpResponseRedirect(reverse('Message_App:room',kwargs={'room_name':  room_name}))

@login_required
def leave_chat(request,room_name):
     c_user =request.user
     
     box = ChatRoom.objects.get(name=room_name)

     success = box.disconnect_user(c_user)
     if success:
          messages.success(request,"Succesfully disconnected")
     return HttpResponseRedirect(reverse('Message_App:inbox'))
