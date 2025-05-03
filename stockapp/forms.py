from django.forms import ModelForm
from django import forms
from . import models

class LoginForm(forms.Form):
    username = forms.CharField(max_length=35, required=True, widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(max_length=25, required=True, widget=forms.PasswordInput(attrs={'class': 'form-input'}))

class AccountForm(ModelForm):
    balance = forms.DecimalField(decimal_places=2)

    account_type = forms.CharField()

    class Meta:
        model = models.Account
        fields = ['balance', 'account_type']
