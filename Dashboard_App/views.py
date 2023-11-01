from binascii import Incomplete
from django.shortcuts import render
from Main_App.models import Post,Bid, Hire
from django.contrib.auth.decorators import login_required

from Work_App.models import Order, RunningWork, Port, Offer
from Account_App.models import Verification

# Create your views here.
@login_required
def dashboard(request):
     if request.user.user_profile.role =='freelancer':
          total_running_order = RunningWork.objects.filter(freelancer=request.user, running=True).count()
          total_active_port = Port.objects.filter(port_author = request.user, active=True).count()
          recent_order_count = Order.objects.filter(freelancer=request.user, status='Placed', payment_status='Pending').count()

          all_act_ports = Port.objects.filter(port_author=request.user, active = True).values('pk')

          all_hires = Hire.objects.filter(port__in = all_act_ports).count()
          return render(request,'freelancer_dash.html',context={'recent_order_count':recent_order_count,'total_running_order':total_running_order, 'total_active_port':total_active_port, 'recent_hires': all_hires })
     
     elif request.user.user_profile.role =='customer':

          total_running_order = RunningWork.objects.filter(customer=request.user, running=True).count()
          total_active_post = Post.objects.filter(post_author = request.user, active=True).count()
          recent_offers = Offer.objects.filter(status='Pending').count

          all_act_posts = Post.objects.filter(post_author=request.user, active = True).values('pk')

          all_bids = Bid.objects.filter(post__in = all_act_posts).count()

          running_order = RunningWork.objects.filter(customer=request.user, running=True)
              # List to store progress items
          progress_items = []

          for work in running_order:
               # Assuming the track field in RunningWork represents the progress percentage
               track_percentage = work.work_track


               # Determine the status based on the track value (you can modify this based on your requirements)
               if track_percentage < 25:
                    status = 'bg-danger'
               elif track_percentage < 50:
                    status = 'bg-warning'
               elif track_percentage < 75:
                    status = 'bg-info'
               else:
                    status = 'bg-success'

               # Append progress item dictionary to the list
               progress_items.append({
                    'percentage': track_percentage,
                    'status': status,
               })
          
          context={'recent_offers':recent_offers,'total_running_order':total_running_order, 'total_active_post':total_active_post, 'recent_bids': all_bids, 'progress_items': progress_items }

          return render(request,'customer_dash.html',context)
     
     elif request.user.user_profile.role =='admin':
          count = Verification.objects.filter(status='Pending').count()
          return render(request,'admin_dash.html',context={'verification_rq_count':  count})





