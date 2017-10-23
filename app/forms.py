"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from app.models import Tempthings

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
        fields = ('description','thing','material','purpose','color','color_combo','scale_info','further_requests',)
        widgets={
            'color_combo':forms.Textarea(attrs={
                'placeholder':'Please tell us how you want the colors combined. Try and keep it simple.'
                }),
            'scale_info':forms.Textarea(attrs={
                'placeholder':'You can define the resizing scale here as a percentage or by giving the value of height, width or length you would like. Please not that the price estimation on the next page assumes no change of scaling and that your part is in mm.'
                }),
            'further_requests':forms.Textarea(attrs={
                'placeholder':'If you have any additional requests for example the direction in which max strength is required which is determined by print orientation, you can make them known here.'
                }),
            }

class EmailForm(forms.Form):
    requestid = forms.IntegerField()
    viable = forms.BooleanField(required=False)
    rejectmessage = forms.CharField(widget=forms.Textarea)



