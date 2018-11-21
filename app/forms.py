"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from app.models import PrintRequest, Quote, Material

class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.pk

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
    first_name = forms.CharField(max_length=30,)
    last_name = forms.CharField(max_length=30,)
    email = forms.EmailField(max_length=254, help_text='Give a valid email address that will be used to send printing info.')
    mobile = forms.CharField(max_length=10, help_text='This will be used to contact you for further queries, if any, and for the exchange.')

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2', 'mobile')

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30,)
    last_name = forms.CharField(max_length=30,)
    email = forms.EmailField(max_length=254,)
    mobile = forms.CharField(max_length=10, help_text='This is the email we’ll use to contact you.')
    username = forms.EmailField(max_length=50, help_text='Used to log into the Cubic3D website')
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email',]

class TempThingForm(forms.ModelForm):
    material = MyModelChoiceField(queryset=Material.objects.all(),initial="PLA")
    #color = forms.ChoiceField(initial = Material.objects.get(acronym='PLA').color1)
    class Meta:
        model = PrintRequest
        fields = ('description','thing','material','purpose','color','color_combo','quantity','further_requests',)
        widgets={
            'color':forms.Select(),
            'color_combo':forms.Textarea(attrs={
                'placeholder':'Please tell us how you want the colors combined. Try and keep it simple.'
                }),
            'further_requests':forms.Textarea(attrs={
                'placeholder':'If you have any additional requests for example the number of pieces otherwise assumed to be 1, you can make them known here.'
                }),
            }

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ('thing','material','purpose','color')
        widgets = {'color':forms.Select()}

class EmailForm(forms.Form):
    price = forms.IntegerField(required=False)
    rejectmessage = forms.CharField(widget=forms.Textarea, required=False)
    add_to_group = forms.BooleanField(required=False, initial=False)
    bill_to = forms.CharField(required=False)

class GroupInvoiceForm(forms.Form):
    bill_to = forms.CharField(required=False)

class ScaleForm(forms.Form):
    scale = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'placeholder':100,'class':'form-control'}))




