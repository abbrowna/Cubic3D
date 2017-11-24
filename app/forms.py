"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from app.models import Tempthings, Quote

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Give a valid email address that will be used to send printing info.')
    mobile = forms.CharField(max_length=10, help_text='This will be used to contact you for further queries, if any, and for the exchange.')

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2', 'mobile')

class TempThingForm(forms.ModelForm):
    class Meta:
        model = Tempthings
        fields = ('description','thing','material','purpose','color','color_combo','further_requests',)
        widgets={
            'color_combo':forms.Textarea(attrs={
                'placeholder':'Please tell us how you want the colors combined. Try and keep it simple.'
                }),
            'further_requests':forms.Textarea(attrs={
                'placeholder':'If you have any additional requests for example the direction in which max strength is required which is determined by print orientation, you can make them known here.'
                }),
            }

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ('thing','material','purpose','color')

class EmailForm(forms.Form):
    viable = forms.BooleanField(required=False)
    price = forms.IntegerField(required=False)
    rejectmessage = forms.CharField(widget=forms.Textarea)

class ScaleForm(forms.Form):
    scale = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'placeholder':100,'class':'form-control'}))




