
from django import forms
from .models import Offer, Order, RunningWork
from django.forms.widgets import DateTimeInput

from Main_App.widgets import BootstrapDateTimePickerInput
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget, AdminSplitDateTime
from datetime import datetime
from .models import RunningWorkFiles, Report
from django.utils.timezone import now

class DateTimeInput(forms.DateTimeInput):

        input_type = 'datetime'

        def get_context(self, name, value, attrs):
                attrs.setdefault('min', now().strftime('%Y-%m-%d %H:%M'))
                return super().get_context(name, value, attrs)


class DateInput(forms.DateInput):
    input_type = 'date'
    def get_context(self, name, value, attrs):
                attrs.setdefault('min', now().strftime('%Y-%m-%d'))
                return super().get_context(name, value, attrs)


class NewOfferForm(forms.ModelForm):

     expected_time = forms.DateField(required=True, widget=DateInput(attrs={ 'value':datetime.now(), 'placeholder':'Expected Time', 'style':'margin:0 0; width: 50%;', 'class': 'form-control'}))
     description = forms.CharField(required=True,label="",widget=forms.Textarea(attrs={'rows':10, 'cols':50, 'placeholder':'Description...', 'style':'margin:15px 0;', 'class': 'form-control'}))

     class Meta:
          model = Offer
          exclude = ['customer','freelancer', 'status']

     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'] = forms.IntegerField(max_value=200000, min_value=50, required=True,label="",widget=forms.NumberInput(attrs={'placeholder':'৳ Offer Amount', 'style':'margin:15px 0; width: 50%;', 'class': 'form-control'}))
        self.fields['support'] = forms.IntegerField(max_value=100, min_value=1, required=True,label="",widget=forms.NumberInput(attrs={'placeholder':'Support', 'style':'margin:15px 0; width: 50%;', 'class': 'form-control'}))  


class OrderForm(forms.ModelForm):
     instruction = forms.CharField(required=True,label="",widget=forms.Textarea(attrs={'rows':10, 'cols':50, 'placeholder':'Instructions...', 'style':'margin:15px 0;', 'class': 'form-control'}))
     deadline = forms.DateTimeField(widget=DateTimeInput(attrs={'type':"datetime-local", 'value':datetime.today(), 'class': 'form-control'}))
     class Meta:
          model = Order
          exclude = ['customer','freelancer','offer_id', 'status', 'payment_status' ]



     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'] = forms.IntegerField(max_value=200000, min_value=50, required=True,label="",widget=forms.NumberInput(attrs={'placeholder':'৳ Order Amount', 'style':'margin:15px 0; width: 50%;', 'class': 'form-control'}))


class RunningWorkForm(forms.ModelForm):
     class Meta:
          model = RunningWork
          fields = ['running',]



class WorkFileForm(forms.ModelForm):
        class Meta:
          model = RunningWorkFiles
          fields = ['file',]


class ReportForm(forms.ModelForm):
        subject = forms.CharField(required=True,label="",widget=forms.TextInput(attrs={'placeholder':'Subject', 'style':'margin:15px 0;', 'class': 'form-control'}))
        body = forms.CharField(required=True,label="",widget=forms.Textarea(attrs={'rows':10, 'cols':30, 'placeholder':'Experience...', 'style':'margin:15px 0;', 'class': 'form-control'}))

        class Meta:
                model = Report
                fields = ['subject', 'body',]