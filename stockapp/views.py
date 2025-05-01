from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views import View
from . import models, forms

# Create your views here.
def home(request):
    '''Home page view'''
    return render(request, 'home.html')

class LoginView(View):
    def get(self, request):
        form = forms.LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            authenticated_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if authenticated_user:
                # Redirect to a success page or dashboard
                return HttpResponse("Login successful.")
        return render(request, 'login.html', {'form': form})

class RegisterView(View):
    def get(self, request):
        form = forms.LoginForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                # Redirect to a success page or dashboard
                return HttpResponse("Registration successful.")

        return render(request, 'register.html', {'form': form})

class AccountView(View):
    def get(self, request):
        form = forms.AccountForm()
        return render(request, 'account.html', {'form': form})

    def post(self, request):
        form = forms.AccountForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Account information saved.")
        return render(request, 'account.html', {'form': form})

    def account_form(self, request):
        if request.method == 'POST':
            form = forms.AccountForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponse("Account information saved.")
        else:
            form = forms.AccountForm()
        return render(request, 'account.html', {'form': form})
