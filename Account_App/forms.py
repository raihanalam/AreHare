from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

from datetime import datetime

from .models import UserProfile, Verification
User = get_user_model()
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from django.utils.timezone import now


class SignInForm(AuthenticationForm):
     username = forms.EmailField(required=True, label="", widget=forms.EmailInput(
         attrs={'placeholder': 'Email', 'style': 'margin-bottom:15px; padding:5px; width: 100%;', 'class': 'form-control'}))
     password = forms.CharField(required=True, label="", widget=forms.PasswordInput(
         attrs={'placeholder': 'Password', 'style': 'margin-bottom:15px; padding:5px; width: 100%;', 'class': 'form-control'}))

     class Meta:
          model = User
          fields = ['username', 'password', ]


class SignUpForm(UserCreationForm):
     email = forms.EmailField(required=True, label="", widget=forms.EmailInput(attrs={
                              'placeholder': 'Email', 'style': 'margin-bottom:20px; padding:5px; width: 100%;', 'class': 'form-control'}))
     username = forms.CharField(required=True, label="", widget=forms.TextInput(
         attrs={'placeholder': 'Username', 'style': 'margin-bottom:20px; padding:5px; width: 100%;', 'class': 'form-control'}))

     password1 = forms.CharField(required=True, label="", widget=forms.PasswordInput(
         attrs={'placeholder': 'Password', 'style': 'margin-bottom:20px; padding:5px; width: 100%;', 'class': 'form-control'}))
     password2 = forms.CharField(required=True, label="", widget=forms.PasswordInput(
         attrs={'placeholder': 'Confirm Password', 'style': 'margin-bottom:20px; padding:5px; width: 100%;', 'class': 'form-control'}))
     captcha = ReCaptchaField(required=True, label="", widget=ReCaptchaV2Checkbox())

     class Meta:
          model = User
          fields = ('username', 'email', 'password1', 'password2','captcha')


class UserProfileChange(UserChangeForm):
     email = forms.EmailField(required=True,label="", widget=forms.TextInput(attrs={
                              'placeholder': 'Email', 'style': 'margin-bottom:10px; padding:5px; width: 300px;', 'class': 'form-control'}))
     username = forms.EmailField(required=True,label="", widget=forms.TextInput(attrs={
                              'placeholder': 'Username', 'style': 'margin-bottom:10px; padding:5px; width: 300px;', 'class': 'form-control'}))
     # username = forms.CharField(required=True,label="Username",widget=forms.TextInput(attrs={'placeholder':'Username', 'style':'margin-bottom:10px; padding:5px; width: 300px;', 'class': 'form-control'}))
     # first_name = forms.CharField(required=True,label="First Name",widget=forms.TextInput(attrs={'placeholder':'First Name', 'style':'margin-bottom:10px; padding:5px; width: 300px;', 'class': 'form-control'}))
     # last_name = forms.CharField(required=True,label="Last Name",widget=forms.TextInput(attrs={'placeholder':'Last Name', 'style':'margin-bottom:10px; padding:5px; width: 300px;', 'class': 'form-control'}))
     password = None
     """password = forms.CharField(required=True,label="",widget=forms.PasswordInput(attrs={'placeholder':'Password'}))"""

     class Meta:
          model = User
          fields = ('username', 'email',)
     # class Meta:
     #      model = User
     #      fields = ('username','email','first_name','last_name','password')

class DateInput(forms.DateInput):
     input_type = 'date'
     
     def get_context(self, name, value, attrs):
          attrs.setdefault('max', now().strftime('%Y-%m-%d'))
          return super().get_context(name, value, attrs)

class UserDetailsInfoChange(forms.ModelForm):
     full_name = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'Full Name', 'style':'margin:15px 0;', 'class': 'form-control'}))
     bio = forms.CharField(label="",widget=forms.Textarea(attrs={'placeholder':'About yourself...', 'style':'margin:15px 0;', 'class': 'form-control'}))
     address_1 = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'Address', 'style':'margin:15px 0;', 'class': 'form-control'}))
     zipcode = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'Zipcode', 'style':'margin:15px 0;', 'class': 'form-control'}))
     city = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'City', 'style':'margin:15px 0;', 'class': 'form-control'}))
     country = CountryField().formfield()
     phone = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'Phone', 'style':'margin:15px 0;', 'class': 'form-control'}))

     university_name = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'University/College Name', 'style':'margin:15px 0;', 'class': 'form-control'}))
     degree = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'Degree', 'style':'margin:15px 0;', 'class': 'form-control'}))
     company_name = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'Company Name', 'style':'margin-bottom:15px;', 'class': 'form-control'}))
     designation = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'Designation', 'style':'margin-bottom:15px;', 'class': 'form-control'}))

     # 'value':datetime.now()
     dob = forms.DateField(label="Date of birth", widget=DateInput(attrs={ 'placeholder':'Date of birth', 'style':'margin-bottom:15px;', 'class': 'form-control'}))
     class Meta:
          model = UserProfile
          
          fields = ('full_name', 'bio', 'address_1', 'zipcode', 'city', 'country',
                    'phone', 'university_name', 'degree', 'company_name', 'designation', 'dob')
          # widgets = {'country': CountrySelectWidget(attrs={'placeholder':'Country', 'style':'margin:15px 0; height:50px; width:80%;', 'class': 'form-control'})}


class UserRole(forms.ModelForm):
     role_choice = (('customer', 'Customer'), ('freelancer', 'Freelancer'))
     role = forms.ChoiceField(required=True, choices=role_choice, label="", widget=forms.RadioSelect(
         attrs={'style': 'margin-bottom:10px;','class': 'd-flex align-items-center justify-content-between', 'required': 'True'}))

     class Meta:
          model = UserProfile
          fields = ['role', ]


class ProfilePic(forms.ModelForm):
     class Meta:
          model = UserProfile
          fields = ['profile_pic', ]


class VerificationForm(forms.ModelForm):
     subject = forms.CharField(required=True,label="Subject",widget=forms.TextInput(attrs={'value':'Applying for profile verification', 'style':'margin:15px 0;', 'class': 'form-control'}))
     application = forms.CharField(required=True,label="Body",widget=forms.Textarea(attrs={'rows':10, 'cols':30, 'value':'Hello, I am writing an application to verfy my given information to AreHare.', 'style':'margin:15px 0;', 'class': 'form-control'}))

     class Meta:
          model = Verification
          fields = ['subject', 'application']


class SetPasswordForm(SetPasswordForm):
     new_password1 = forms.CharField(required=True, label="", widget=forms.PasswordInput(attrs={'placeholder': 'New Password', 'style': 'margin-bottom:10px; padding:5px; width: 100%;', 'class': 'form-control'}))
     new_password2 = forms.CharField(required=True, label="", widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password', 'style': 'margin-bottom:10px; padding:5px; width: 100%;', 'class': 'form-control'}))

     class Meta:
          model = get_user_model()
          fields = ['new_password1', 'new_password2']

class PasswordResetForm(PasswordResetForm):
     email = forms.EmailField(required=True, label="", widget=forms.EmailInput(attrs={'placeholder': 'Email', 'style': 'margin-bottom:20px; padding:5px; width: 100%;', 'class': 'form-control'}))
     def __init__(self, *args, **kwargs):
          super(PasswordResetForm, self).__init__(*args, **kwargs)

     captcha = ReCaptchaField(required=True, label="", widget=ReCaptchaV2Checkbox())

     
