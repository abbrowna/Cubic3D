"""
Definition of forms for the store.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)

from store.models import Filament, Order 
from app.models import Profile

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Email'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class FilterForm(forms.ModelForm):
    class Meta:
        model = Filament
        fields = ['diameter','material']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'address', 'company', 'region', 'email', 'alt_name', 'alt_phone']
        widgets = {
            'address':forms.Textarea(attrs = {'placeholder':'Enter a full physical address for delivery'}),
            'phone':forms.TextInput(attrs = {'placeholder':'07'}),
            'company':forms.TextInput(attrs = {'placeholder':'Optional'}),
            'email':forms.TextInput(attrs = {'placeholder':'example@domain.com'})
        }


class SignUpForm(UserCreationForm):
    error_css_class = 'error'
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','placeholder':'Enter a strong password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','placeholder':'Repeat password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')
        widgets = {
            'email':forms.TextInput(attrs = {'placeholder':'example@domain.com'}),
            'first_name':forms.TextInput(attrs = {'placeholder':'First name'}),
            'last_name':forms.TextInput(attrs = {'placeholder':'Last name'}),
            'password1':forms.PasswordInput(attrs = {'placeholder':'Enter a strong password'}),
            'password2':forms.PasswordInput(attrs = {'placeholder':'Repeat password'})
        }
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            self.add_error('email',"A user with this email already exists")
        return self.cleaned_data

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('address', 'mobile', 'company', 'region')
        widgets = {
            'address':forms.Textarea(attrs = {'placeholder':'Enter a default physical address for delivery'}),
            'mobile':forms.TextInput(attrs = {'placeholder':'Mobile number 07'}),
            'company':forms.TextInput(attrs = {'placeholder':'Company name (Optional)'}),
        }
        