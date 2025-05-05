import os
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from stockapp.forms import AccountForm
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
    accounts = models.Account.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {
        'user': request.user,
        'stockapp_accounts': accounts  # Add this line
    })

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
                login(request, authenticated_user)
                return redirect('dashboard')
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
                login(request, user)
                return redirect('dashboard', {'user': user})

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

@login_required
def addaccount(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
        return redirect('dashboard')
    return render(request, 'account.html', {'form': AccountForm})


class AccountListView(ListView):
    model = models.Account
    context_object_name = 'stockapp_accounts'
    def get_queryset(self):
        #only for currently logged in users
        return models.Account.objects.filter(user=self.request.user)
