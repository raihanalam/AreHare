from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, SetPasswordForm

# For emailing
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from django.db.models.query_utils import Q

# Custom
from Account_App.models import UserProfile
from . forms import SignInForm, SignUpForm, User, UserDetailsInfoChange, UserProfileChange, ProfilePic, UserRole, VerificationForm, PasswordResetForm, SetPasswordForm
from .decorators import user_not_authenticated
from .tokens import account_activation_token
import re


from Work_App.models import CompleteWork
from django.db.models import Avg

# Create your views here.

@user_not_authenticated
def sign_up(request):

    form = SignUpForm()
    form1 = UserRole()

    registerd = False
    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        form1 = UserRole(data=request.POST)

        if form.is_valid() and form1.is_valid():
            user = form.save(commit=False)

            x = re.search(" ", user.username)
            regex = re.compile('[@!#$%^&*()<>?/\|}{~: .,"`]')

            if regex.search(user.username):
                messages.warning(request, 'Username can not hold space or special character.')
            else:
                user.is_active = False
                user.save()
                roleForm = form1.save(commit=False)
                roleForm.user = user
                roleForm.save()
                activateEmaill(request, user, form.cleaned_data.get('email'))
                registerd = True
                return redirect('Account_App:signin')    

    dict = {'form': form, 'form1': form1, 'registerd': registerd}
    return render(request, 'signup.html', context=dict)


@user_not_authenticated
def sign_in(request):
    form = SignInForm()

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('Main_App:home_page'))

    return render(request, 'signin.html', context={'form': form})


@login_required
def sign_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def user_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)

    return render(request, 'profile.html', context={'user_profile': user_profile})


@login_required
def user_profile_change(request):
    current_user = request.user
    user_profile = UserProfile.objects.get(user=current_user)
    form = UserDetailsInfoChange(instance=user_profile)

    if request.method == "POST":
        form = UserDetailsInfoChange(request.POST, instance=user_profile)

        if form.is_valid():
            form.save()
            form = UserDetailsInfoChange(instance=user_profile)
            messages.success(request, 'Profile information updated.')

    return render(request, 'user_profile_change.html', context={'form': form})


@login_required
def change_profile(request):
    current_user = request.user

    form = UserProfileChange(instance=current_user)
    if request.method == "POST":
        form = UserProfileChange(request.POST, instance=current_user)

        if form.is_valid():
            form.save()
            form = UserProfileChange(instance=current_user)
            messages.success(request, 'Personal information updated.')

    return render(request, 'change_profile.html', context={'form': form})


@login_required
def change_password(request):
    current_user = request.user
    form = PasswordChangeForm(current_user)

    if request.method == "POST":
        form = PasswordChangeForm(current_user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password has been changed.')

    return render(request, 'change_password.html', context={'form': form})


@login_required
def add_pro_pic(request):
    form = ProfilePic()

    if request.method == "POST":

        form = ProfilePic(request.POST, request.FILES,
                          instance=request.user.user_profile)

        if form.is_valid():
            form.save()
            '''user_obj = form.save(commit=False)
               user_obj.user = request.user
               user_obj.save() #commit true default'''
            return HttpResponseRedirect(reverse('Account_App:profile'))

    return render(request, 'add_pro_pic.html', context={'form': form})


@login_required
def change_pro_pic(request):
    form = ProfilePic(instance=request.user.user_profile)
    if request.method == "POST":
        form = ProfilePic(request.POST, request.FILES,
                          instance=request.user.user_profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('Account_App:profile'))

    return render(request, 'add_pro_pic.html', context={'form': form})


def settings(request):
    return render(request, 'settings.html')


def activateEmaill(request, user, to_email):

    mail_subject = "Activate your user account."
    message = render_to_string("template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })

    email = EmailMessage(mail_subject, message, to=[to_email])

    if email.send():
        messages.success(
            request, f'Dear {user.username}, please check your email {to_email} inbox and click on activation link to confirm and complete the registration. \n Note: Check your spam folder.')
    else:
        messages.error(
            request, f'Problem sending email to {to_email}, check if you typed it correctly.')


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(
            request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('Account_App:signin')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('Account_App:signin')


def profile_verification(request):

    form = VerificationForm()

    if request.method == 'POST':
        form = VerificationForm(request.POST)

        if form.is_valid():
            p_v = form.save(commit=False)
            p_v.user = request.user
            p_v.save()
            form = VerificationForm()
            messages.info(request, 'Your application has been send. Please wait for verification')
            # return HttpResponseRedirect('')

    return render(request, 'verification_form.html', context={'form': form})


@user_not_authenticated
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset request"
                message = render_to_string("template_reset_password.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[
                                     associated_user.email])
                if email.send():
                    messages.success(request,
                                     """
                            We've emailed you instructions for setting your new password. 
                            If you entered a valid email, you should receive it shortly. If you don't receive an email, please ensure you've entered the address you registered with.
                            Note: Check your spam folder as well.
                        """
                                     )
                else:
                    messages.error(
                        request, "Problem sending reset password email'")

            return redirect('index')

        for key, error in list(form.errors.items()):
            if key == 'captcha' and error[0] == 'This field is required.':
                messages.error(request, "You must pass the reCAPTCHA test")
                continue

    form = PasswordResetForm()
    return render(
        request=request,
        template_name="password_reset.html",
        context={"form": form}
    )

# @user_not_authenticated


def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(
                    request, "Your password has been set. You may go ahead and <b>log in </b> now.")
                return redirect('Account_App:signin')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, "Link is expired")

    messages.error(
        request, 'Something went wrong, redirecting back to Homepage')
    return redirect("index")


def signup_redirect(request):
    messages.error(request, "Something wrong here, it may be that you already have account!")
    return redirect("index")



@login_required
def user_profile_view(request,username):
    other_user = User.objects.get(username=username)
    total_work = CompleteWork.objects.filter(freelancer=other_user, completed=True).count()

    ratings = other_user.freelancer_profile_ratings.all()



    rating_average = ratings.aggregate(Avg('rating'))['rating__avg'] if ratings.aggregate(Avg('rating'))['rating__avg'] else 0
     
    print(total_work)

    # if other_user == request.user:
    #       return HttpResponseRedirect(reverse('Account_App:profile'))
    return render(request,'user.html',context={'profile':other_user, 'total_work': total_work, 'rating_average': rating_average})
