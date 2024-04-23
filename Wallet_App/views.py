from django.dispatch import receiver
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from Work_App.forms import OrderForm

from Work_App.models import Offer, Order

from notifications.signals import notify


# #Models and Forms
from .models import Deposits, Payment, PendingPayment, Transaction, UserWallet, Wallet, WithdrwalRequest
from .forms import DepositForm, PendingPaymentForm, UserWalletForm, WithdrawRequestForm

#For canceling CSRF Checking
from django.views.decorators.csrf import csrf_exempt

#Payment
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal


# Create your views here.
@login_required
def wallet(request):
     obj = {}
     try:
          obj = UserWallet.objects.get(user=request.user)
     except:
          forms = UserWalletForm()

     if obj:

          return render(request, 'wallet.html', context={'wallet': obj})
     else:
          if request.method == 'POST':
               wallet_data_form = UserWalletForm(request.POST, request.FILES)
               if wallet_data_form.is_valid():
                    wallet = wallet_data_form.save(commit=False)
                    wallet.user = request.user
                    wallet.active = True
                    wallet.save()

                    #Getting the saved UserWallet Bluprint
                    n_W_obj = UserWallet.objects.get(user=request.user)
                    
                    #Creating the actual Wallet
                    wallet_ob = Wallet()
                    wallet_ob.user= request.user
                    wallet_ob.u_w= n_W_obj
                    wallet_ob.currency= n_W_obj.currency
                    wallet_ob.save()
                    return HttpResponseRedirect(reverse('Wallet_App:wallet_page'))

          # messages.warning(request, 'Your wallet is not active please complete wallet form.')
          return render(request, 'wallet.html', context={'forms':forms})






# Deposit process for customer account
@login_required
def deposit_checkout(request):
     wallet = Wallet.objects.get(user = request.user )
     exist_unsuccess_deposit = Deposits.objects.get_or_create(user = request.user, success=False, wallet_id = wallet )

     exist_unsuccess_deposit = exist_unsuccess_deposit[0]

     form = DepositForm(instance=exist_unsuccess_deposit)
     if request.method == "POST":
          form = DepositForm(request.POST,instance=exist_unsuccess_deposit)
          if form.is_valid():
               form.save()
               form = DepositForm(instance=exist_unsuccess_deposit)
               messages.success(request, 'Deposit form filled! You can confirm deposit now!')
     
     deposit = Deposits.objects.get(user = request.user , success =False)

     if deposit.amount >= 200 and deposit.reference != '':
          eligable = True
     else:
          eligable = False

     return render(request, 'deposit_checkout.html', context={'form':form, 'deposit': deposit, 'eligable':eligable})

@login_required
def confirm_deposit(request):
     wallet = Wallet.objects.get(user = request.user )
     deposits = Deposits.objects.get(user = request.user, success=False, wallet_id = wallet)

     if deposits.amount <= 199 and deposits.reference !='':
          messages.info(request,f"Please complete deposit more then Tk 199!")
          return redirect("Wallet_App:deposit_checkout")

     if not request.user.user_profile.is_fully_filled():
          messages.info(request,f"Please complete all information of your profile.")
          return redirect('Account_App:profile')

     #SSLCommerz Store ID
     store_id = 'areha6581f2f97971c'
     #API key
     store_pass = 'areha6581f2f97971c@ssl'
     
     status_url = request.build_absolute_uri(reverse("Wallet_App:deposit_complete"))

     mydeposit = SSLCSession(sslc_is_sandbox=True, sslc_store_id= store_id, sslc_store_pass=store_pass)
     mydeposit.set_urls(success_url=  status_url, fail_url=  status_url, cancel_url=  status_url, ipn_url=  status_url)


     deposit_total = deposits.amount

     mydeposit.set_product_integration(total_amount=Decimal(deposit_total), currency='BDT', product_category='Mixed', product_name="Deposit", num_of_item=1, shipping_method='On', product_profile='None')


     current_user = request.user

     mydeposit.set_customer_info(name=current_user.user_profile.full_name, email=current_user.email, address1=current_user.user_profile.address_1, address2=current_user.user_profile.address_1, city=current_user.user_profile.city, postcode=current_user.user_profile.zipcode, country=current_user.user_profile.country, phone=current_user.user_profile.phone)
     mydeposit.set_shipping_info(shipping_to=current_user.user_profile.full_name, address=current_user.user_profile.address_1, city=current_user.user_profile.city, postcode=current_user.user_profile.zipcode, country=current_user.user_profile.country)


     response_data = mydeposit.init_payment()
     #print(response_data)
     return redirect(response_data['GatewayPageURL'])


@csrf_exempt
def deposit_complete(request):
     payment_data = request.GET

     if request.method == 'POST' or request.method == 'post':
          payment_data = request.POST
          status = payment_data['status']

          if status == 'VALID':
               val_id = payment_data['val_id']
               tran_id = payment_data['tran_id']
               bank_tran_id = payment_data['bank_tran_id']
               tran_date = payment_data['tran_date']
               payment_type = payment_data['card_type']
               
               messages.success(request,f'Your deposit is successfully done by {payment_type}')

               return HttpResponseRedirect(reverse('Wallet_App:deposit_transaction', kwargs={'val_id':val_id, 'tran_id':tran_id, 'payment_type':payment_type}))

          elif status == 'FAILED':
               messages.warning(request,f'Your deposit Failed! Please try again.')
               return HttpResponseRedirect(reverse('Wallet_App:wallet_page'))
               
          elif status == 'CANCELLED':
               messages.warning(request,f'OOPS! You canceled your deposit, Please try again.')
               return HttpResponseRedirect(reverse('Wallet_App:wallet_page'))
          else:
               messages.warning(request, 'There is an error with this payment. Try again later.')
     else:
          messages.warning(request, 'The payment is not succeed. Try again later.')

     # return render(request,'deposit_complete.html',context={})
     return HttpResponseRedirect(reverse('Wallet_App:wallet_page'))



@login_required
def deposit_transaction(request, val_id, tran_id, payment_type):

     wallet = Wallet.objects.get(user=request.user)
     deposit = Deposits.objects.get(user=request.user, success = False)


     transaction_id = tran_id

     deposit.trans_id = transaction_id
     deposit.success = True
     deposit.wallet_id = wallet
     deposit.val_id = val_id
     deposit_amount = deposit.amount
     deposit.payment_type = payment_type
    
     
     amount = deposit_amount
     type = 'deposit'
     receiver = request.user

     success = transaction_process(request, type, amount,'', receiver)
     if success:
          deposit.save()
          messages.success(request, f'Your wallet balance increased {amount}')
     
     return HttpResponseRedirect(reverse('Wallet_App:wallet_page'))

@login_required
def transaction_process(request, type, amount, sender, receiver):
     
     if type == 'deposit':
          receiver_wallet = Wallet.objects.get(user = receiver)
          receiver_wallet.credit(amount)
          receiver_wallet.save()

          transaction = Transaction(wallet=receiver_wallet, transaction_type='CREDIT', amount = amount)
          transaction.save()

          return True

     if type == 'payment':
          sender_wallet = Wallet.objects.get(user = sender)
          
          status = sender_wallet.debit(amount)

          if status == True:
               sender_wallet.save()
               transaction = Transaction(wallet=sender_wallet, transaction_type='DEBIT', amount = amount)
               transaction.save()

               return True

     return False



@login_required
def order_checkouts(request, order_id):
     order = Order.objects.get(id=order_id, customer = request.user, status='Created',payment_status='Checkout')
     offer = Offer.objects.get(id = order.offer_id.id)

     order_total = order.get_totals()

     return render(request, 'payment_checkout.html', context={'offer_details':offer,'order_details': order, 'order_total':order_total})

def payment_confirm(request,order_id):
     pay_q = PendingPaymentForm()
     order = Order.objects.get(id=order_id, customer = request.user)
     wallet = Wallet.objects.get(user=request.user)
     offer = Offer.objects.get(id=order.offer_id.id)

     if request.method == 'POST':
          if wallet.balance >= order.amount:
               pay_ment = PendingPaymentForm(request.POST)
               if pay_ment.is_valid():
                    pay = pay_ment.save(commit=False)
                    if pay.confirmation == True:
                         pay.user_id = request.user
                         pay.order_id = order
                         pay.amount = order.amount
                         pay.confirmation = True
                         pay.save()
                         offer.status = 'Accepted'
                         order.status = 'Placed'
                         order.payment_status = 'Pending'
                         
                         offer.save()
                         order.save()
                         
                         notify.send(request.user, recipient = order.freelancer, verb=f"{order.customer.username} placed an order.")
                         messages.success(request,f'Your payment is confirmed, wait for order accepted.')
                         return HttpResponseRedirect(reverse('Work_App:all_orders'))
                    else:
                         messages.warning(request, f'Please check the confirmation box!')
          else:
               messages.warning(request, 'Your balance is too low, please deposit some money.')


     if order.payment_status == 'Checkout':
          return render (request, 'payment_confirm.html', context={'order': order, 'payq_form':pay_q})
     else:
          messages.success(request,f'This payment is not available')
          return HttpResponseRedirect(reverse('Wallet_App:wallet_page'))


@login_required
def payment_complete(request, order_id):
     order = Order.objects.get(id=order_id, customer = request.user)
     pending_payment = PendingPayment.objects.get(user_id=request.user, order_id=order)
     
     new_payment = Payment(sender=request.user, receiver=order.freelancer, amount= pending_payment.amount, success_url=True)
     new_payment.save()

     success = payment_transaction(request, new_payment.id)

     if success == True:
          order.payment_success = True
          pending_payment.success = True
          pending_payment.save()
          order.save()

          notify.send(request.user, recipient = order.freelancer, verb=f'''<p> You got a payment from {order.customer.username} <a href="/wallet/">Check</a> ''')
          messages.success(request, f'Your payment is successfully done from wallet.')

     return HttpResponseRedirect(reverse('Wallet_App:wallet_page'))
    

@login_required
def payment_transaction(request, payment_id):

     payment = Payment.objects.get(id=payment_id)

     payment_type = 'payment'
     deposit_type = 'deposit'

     amount = payment.amount

     sender = request.user
     receiver = payment.receiver

     payment_process = transaction_process(request, payment_type, amount, sender, '')
     deposit_process = transaction_process(request, deposit_type, amount, '', receiver)
     
     if payment_process == True and deposit_process == True:
          payment.success_url = True
          payment.save()
          return True
     else:
          return False


@login_required
def unsuccess_checkouts(request):
     unsuccess_checkouts = Order.objects.filter(customer=request.user, payment_status='Checkout')

     return render(request,'unsuccess_checkouts.html',context={'unsuccess_checkouts':unsuccess_checkouts})


@login_required
def withdraw_request(request):
     form = WithdrawRequestForm()
     user_wallet = Wallet.objects.get(user=request.user)
     exist_unsuccess_withdrwals = WithdrwalRequest.objects.get_or_create(user = request.user, confirms=False, wallet = user_wallet)
     exist_unsuccess_withdrwal = exist_unsuccess_withdrwals[0]

     form = WithdrawRequestForm(instance=exist_unsuccess_withdrwal)
     if request.method == 'POST':
          withdraw_form = WithdrawRequestForm(request.POST, instance=exist_unsuccess_withdrwal)
          if withdraw_form.is_valid():
               withdraw = withdraw_form.save(commit=False)
               withdraw.calculate_network_fee()
               withdraw.save()
               form = WithdrawRequestForm(instance=exist_unsuccess_withdrwal)

     withdrawal = exist_unsuccess_withdrwals[0]
     eligable =False
     if withdrawal.amount <= user_wallet.balance:
          withdraw_request = WithdrwalRequest.objects.filter(user = request.user, confirms=True, complete=False)
          requested_amount = 0
          for w in withdraw_request:
               requested_amount += w.amount
          
          current_balance = user_wallet.balance - requested_amount

          if requested_amount <= user_wallet.balance:
               if current_balance >= withdrawal.amount and withdrawal.amount >= 2000:
                    eligable = True
                    messages.success(request, 'Withdrwal form filled! You can now send request')
               elif withdrawal.amount < 2000:
                    messages.warning(request, 'You can only withdraw minimum 2000 tk. ')
               else:
                    messages.warning(request, 'Your requeste is not possible, you have pending withdrwals or your balance does not have enough money. ')
          else:
               messages.warning(request, 'You have already pending request which is equal to your balance.')
     else:
          eligable = False
          messages.warning(request, 'Your requeste is not possible, your balance does not have enough money.')

     return render(request, 'withdraw_request.html', context={'form': form, 'withdrawal':withdrawal, 'eligable':eligable})

@login_required
def confirm_withdraw(request, pk):
     withdraw = WithdrwalRequest.objects.get(user=request.user, pk=pk)
     withdraw.confirms = True
     withdraw.status = "pending"
     withdraw.save()
     messages.success(request, 'Your withdrwal request is pending now. Wait for while processing!')

     return HttpResponseRedirect(reverse('Wallet_App:all_withdraw'))
     

@login_required
def all_withdraw(request):
     all_withdrawals = WithdrwalRequest.objects.filter(user= request.user, confirms=True)

     return render(request, 'all_withdrwals.html', context={'all_withdrwals': all_withdrawals })

@login_required
def all_deposts_list(request):
     deposits = Deposits.objects.filter(user = request.user, success=True)

     return render(request, 'all_deposits_lists.html', context={'all_deposits': deposits})

@login_required
def all_payment_list(request):
     payments = Payment.objects.filter(sender = request.user, success_url=True)

     return render(request, 'all_payment_list.html', context={'all_payments': payments})


@login_required
def pending_payment_list(request):
     pending_payments = PendingPayment.objects.filter(user_id = request.user, confirmation=True, success=False)

     return render(request, 'pending_payment.html', context={'pending_payments': pending_payments})


@login_required
def all_transaction_list(request):

     return render(request, 'all_transaction.html')

