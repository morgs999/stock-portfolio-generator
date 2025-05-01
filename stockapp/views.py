import os
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views import View
from django.contrib.auth.decorators import login_required
from . import models, forms

def home(request):
    """Home Page"""
    stock_data = get_data_from_polygon(request, inclusion=True)
    return render(request, 'home.html', stock_data)

def get_data_from_polygon(request, inclusion=False):
    api_key = os.environ.get('POLYGON_API_KEY', '')
    url = f'https://api.polygon.io/v3/reference/tickers?ticker=GOOG&market=stocks&active=true&order=asc&limit=100&sort=ticker&apiKey={api_key}'
    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        data = response.json()
        context = {'data': data}
    else:
        error_message = f"API Error: {response.status_code} - {response.text}"
        context = {'error': error_message}

    if inclusion:
        return context

    return render(request, 'stock.html', context)

@login_required
def dashboard(request):
    """User Dashboard"""
    return render(request, 'dashboard.html')

def logout_view(request):
    """User Logout"""
    logout(request)
    return redirect('home')

class LoginView(View):
    def get(self, request):
        form = forms.LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            authenticated_user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if authenticated_user:
                # Redirect to a success page or dashboard
                # return HttpResponse("Login successful.")
                login(request, authenticated_user)
                return redirect('home')
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
