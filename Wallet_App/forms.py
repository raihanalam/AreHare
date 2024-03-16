from pyexpat import model
from attr import field
from django import forms
from .models import Deposits, PendingPayment, UserWallet, WithdrwalRequest, Currency


class UserWalletForm(forms.ModelForm):
     identiy_choices = (
          ('nid', 'National Identity'),
          ('passport', 'Passport'),

     )
     identity_type = forms.ChoiceField(choices=identiy_choices)
     identity_number = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'Identity Number', 'style':'margin:15px 0; width: 100%;', 'class': 'form-control'}))
     identity_image = forms.ImageField(required=True, label="Upload Image File", widget= forms.FileInput(attrs={'placeholder':'Upload Image', 'style':'width:100%; margin-bottom:15px;', 'class': 'form-control'}))

     class Meta:
          
          model = UserWallet
          fields = ['identity_type', 'identity_number','identity_image', 'currency']


class DepositForm(forms.ModelForm):

     class Meta:
          model = Deposits
          fields = ['reference','amount','method',]


class PendingPaymentForm(forms.ModelForm):

     class Meta:
          model = PendingPayment
          fields = ['confirmation',]


class WithdrawRequestForm(forms.ModelForm):
     class Meta:
          model = WithdrwalRequest
          #fields = '__all__'
          exclude = ['user','wallet','network_fee', 'status', 'receivable_amount','confirms', 'complete']
