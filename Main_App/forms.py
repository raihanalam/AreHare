from attr import attr
from django import forms
from django.forms.widgets import ChoiceWidget
from .models import Bid, Hire, Port, ReviewRating, Category, Post, PublicPost
from ckeditor.widgets import CKEditorWidget
# from datetime import datetime
from django.utils.timezone import datetime


from django.utils.timezone import now


class PortForm(forms.ModelForm):
    # port_category = forms.ModelChoiceField(label="",queryset = Category.objects.all(), widget=forms.Select(attrs={'style':'width:100%; height:40px; border:none;','class':'bootstrap-select'}))
    port_category = forms.ModelChoiceField(
        label="",
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={
            'style': 'width: 100%; height: 40px; ',
            'class': 'bootstrap-select p-2 form-select'
        }),
        empty_label='Select a category'  # Custom placeholder option
    )
    port_title = forms.CharField(required=True, label="", widget=forms.TextInput(
        attrs={'placeholder': 'Title', 'style': 'margin:15px 0;', 'class': 'form-control'}))
    expert = forms.CharField(required=True, label="", widget=forms.TextInput(attrs={
                             'placeholder': 'Expertise on', 'style': 'margin:15px 0;', 'class': 'form-control'}))
    skills = forms.CharField(required=True, label="", widget=forms.TextInput(
        attrs={'placeholder': 'Skills', 'style': 'margin:15px 0;', 'class': 'form-control'}))
    # port_description = forms.CharField(required=True,label="", widget=CKEditorWidget(attrs={'placeholder':'Description...', 'style':'margin:15px 0; width:100%;', 'class': 'form-control'}))
    port_description = forms.CharField(
        required=True,
        label="",
        widget=CKEditorWidget(attrs={
            'placeholder': 'Description...',
            'style': 'margin: 15px 0; width: 100%; height: 300px;',  # Adjust the width as needed
            'class': 'form-control',

        }),
     initial='Add description here...'  # Add the default value here


    )

    port_image = forms.ImageField(required=True, label="", widget=forms.FileInput(
        attrs={'placeholder': 'Upload Image', 'style': 'margin:15px 0; width:50%;', 'class': 'form-control', 'title': 'Upload Image',}))
    # rate_amount = forms.IntegerField(required=True,label="",widget=forms.NumberInput(attrs={'placeholder':'৳ Per hour', 'style':'margin:15px 0; width: 50%;', 'class': 'form-control'}))
    keywords = forms.CharField(required=True, label="", widget=forms.TextInput(
        attrs={'placeholder': 'Keywords', 'style': 'margin-bottom:15px; width:50%;', 'class': 'form-control'}))

    class Meta:
        model = Port
        fields = ('port_category', 'port_title', 'expert', 'skills',
                  'port_description', 'port_image', 'rate_amount', 'keywords')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rate_amount'] = forms.IntegerField(max_value=200000, min_value=50, required=True, label="", widget=forms.NumberInput(
            attrs={'placeholder': '৳ Per hour', 'style': 'margin:15px 0; width: 50%;', 'class': 'form-control'}))


class DateInput(forms.DateInput):

    input_type = 'date'

    def get_context(self, name, value, attrs):
        attrs.setdefault('min', now().strftime('%Y-%m-%d'))
        return super().get_context(name, value, attrs)


class PostForm(forms.ModelForm):
    post_category = forms.ModelChoiceField(label="Category", queryset=Category.objects.all(
    ), widget=forms.Select(attrs={'style': 'width:100%; height:40px;', 'class': 'bootstrap-select'}))
    post_title = forms.CharField(required=True, label="", widget=forms.TextInput(
        attrs={'placeholder': 'Job Title', 'style': 'margin:15px 0;', 'class': 'form-control'}))
    required_skills = forms.CharField(required=True, label="", widget=forms.TextInput(
        attrs={'placeholder': 'Skill Required', 'style': 'margin:15px 0;', 'class': 'form-control'}))
    post_description = forms.CharField(required=True, label="Description", widget=CKEditorWidget(
        attrs={'placeholder': 'Description', 'style': 'margin:15px 0; width:100%;', 'class': 'form-control'}))
    deadline = forms.DateField(widget=DateInput(
        attrs={'style': 'margin:15px 0; width:50%;', 'class': 'form-control'}))
    post_image = forms.ImageField(required=False, label="Upload Image File", widget=forms.FileInput(
        attrs={'placeholder': 'Upload Image', 'style': 'width:50%;', 'class': 'form-control'}))
    # budget_amount = forms.IntegerField(required=True,label="",widget=forms.NumberInput(attrs={'placeholder':'৳ Budget', 'style':'margin:15px 0; width: 50%;', 'class': 'form-control'}))
    keywords = forms.CharField(required=False, label="", widget=forms.TextInput(
        attrs={'placeholder': 'Keywords', 'style': 'margin-bottom:15px; width:50%;', 'class': 'form-control'}))

    class Meta:
        model = Post
        fields = ('post_category', 'post_title', 'required_skills',
                  'post_description', 'post_image', 'budget_amount', 'keywords', 'deadline')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['budget_amount'] = forms.IntegerField(max_value=200000, min_value=100, required=True, label="", widget=forms.NumberInput(
            attrs={'placeholder': '৳ Budget', 'style': 'margin:15px 0; width: 50%;', 'class': 'form-control'}))


class BidForm(forms.ModelForm):
    #ports = Port.objects.filter(user=request.user, active=True)
    #port = forms.ChoiceField(choices=[(choice.pk, choice.title) for choice in Port.objects.filter(port_author=request.user, active=True)])

    class Meta:
        model = Bid
        fields = ('bid_note', 'bid_amount')
        widgets = {
            'bid_note': forms.Textarea(attrs={'rows': 5, 'cols': 25}),
        }


class HireForm(forms.ModelForm):
    class Meta:
        model = Hire
        fields = ('hire_message', 'hire_amount')
        widgets = {
            'hire_message': forms.Textarea(attrs={'rows': 5,'class':'form-control'}),
            'hire_amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ReviewForm(forms.ModelForm):

    class Meta:
        model = ReviewRating
        fields = ['rating', 'review']


class PortEditForm(forms.ModelForm):

    port_category = forms.ModelChoiceField(label="", queryset=Category.objects.all(
    ), widget=forms.Select(attrs={'style': 'width:100%; height:40px;', 'class': 'bootstrap-select'}))
    port_title = forms.CharField(label="", widget=forms.TextInput(
        attrs={'placeholder': 'Title', 'style': 'margin:15px 0;', 'class': 'form-control'}))
    expert = forms.CharField(required=True, label="", widget=forms.TextInput(attrs={
                             'placeholder': 'Expertise on', 'style': 'margin:15px 0;', 'class': 'form-control'}))
    skills = forms.CharField(required=True, label="", widget=forms.TextInput(
        attrs={'placeholder': 'Skills', 'style': 'margin:15px 0;', 'class': 'form-control'}))
    port_image = forms.ImageField(required=True, label="Hero Image", widget=forms.FileInput(
        attrs={'placeholder': 'Upload Image', 'style': 'width:50%;', 'class': 'form-control'}))
    port_description = forms.CharField(required=True, label="", widget=CKEditorWidget(
        attrs={'placeholder': 'Skills', 'style': 'margin:15px 0; width:100%;', 'class': 'form-control'}))
    rate_amount = forms.CharField(required=True, label="", widget=forms.NumberInput(
        attrs={'placeholder': '৳ Per hour', 'style': 'margin:15px 0; width: 50%;', 'class': 'form-control'}))
    keywords = forms.CharField(required=True, label="", widget=forms.TextInput(
        attrs={'placeholder': 'Keywords', 'style': 'margin-bottom:15px; width:50%;', 'class': 'form-control'}))

    class Meta:
        model = Port
        fields = ('port_category', 'port_title', 'expert', 'skills',
                  'port_description', 'port_image', 'rate_amount', 'keywords')


class PostEditForm(forms.ModelForm):

    post_category = forms.ModelChoiceField(label="", queryset=Category.objects.all(
    ), widget=forms.Select(attrs={'style': 'width:100%; height:40px;', 'class': 'bootstrap-select'}))
    post_title = forms.CharField(label="", widget=forms.TextInput(
        attrs={'placeholder': 'Title', 'style': 'margin:15px 0;', 'class': 'form-control'}))
    required_skills = forms.CharField(required=True, label="", widget=forms.TextInput(
        attrs={'placeholder': 'Required Skills', 'style': 'margin:15px 0;', 'class': 'form-control'}))
    post_description = forms.CharField(required=True, label="", widget=CKEditorWidget(
        attrs={'placeholder': 'Description...', 'style': 'margin:15px 0; width:100%;', 'class': 'form-control'}))
    post_image = forms.ImageField(required=True, label="Upload Image File", widget=forms.FileInput(
        attrs={'placeholder': 'Upload Image', 'style': 'width:50%;', 'class': 'form-control'}))
    budget_amount = forms.CharField(required=True, label="", widget=forms.NumberInput(
        attrs={'placeholder': '৳  Budget Amount', 'style': 'margin:15px 0; width: 50%;', 'class': 'form-control'}))
    keywords = forms.CharField(required=True, label="", widget=forms.TextInput(
        attrs={'placeholder': 'Keywords', 'style': 'margin-bottom:15px; width:50%;', 'class': 'form-control'}))

    class Meta:
        model = Post
        fields = ('post_category', 'post_title', 'required_skills',
                  'post_description', 'post_image', 'budget_amount', 'keywords')


class PublicPostForm(forms.ModelForm):

    class Meta:
        model = PublicPost
        fields = ('full_name', 'email', 'phone' , 'category','title', 'description', 'files')

        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'cols': 25}),
        }
