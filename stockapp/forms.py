from django import forms
from . import models

class LoginForm(forms.Form):
    username = forms.CharField(max_length=35, required=True, widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(max_length=25, required=True, widget=forms.PasswordInput(attrs={'class': 'form-input'}))

class AccountForm(forms.Form):
    user = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-input'}))

    balance = forms.DecimalField(max_digits=8, decimal_places=2, required=True, widget=forms.NumberInput(attrs={'class': 'form-input', 'min': '0.00', 'step': '0.01'}))

    account_type = forms.ChoiceField(choices=[('checking', 'Checking'), ('savings', 'Savings')], required=True, widget=forms.Select(attrs={'class': 'form-select'}))

    def save(self):
        """Save the form data to the database"""
        account = models.Account(
            user=self.cleaned_data['user'],
            balance=self.cleaned_data['balance'],
            account_type=self.cleaned_data['account_type']
        )
        account.save()
        return account
