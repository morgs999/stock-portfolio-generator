import os
import json
import io
import base64
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv
import pandas as pd

from stockapp.forms import AccountForm
from . import models, forms

matplotlib.use('Agg')
load_dotenv()


def home(request):
    """Home Page"""
    data = get_data(request, inclusion=True)
    print('home page data', data)
    return render(request, 'home.html', data)


def simple_plot(request):
    x = np.linspace(0, 2 * np.pi, 200)
    y = np.sin(x)

    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_title('Sine Wave')
    ax.set_xlabel('Z')
    ax.set_ylabel('Y')

    # Save to a string buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Convert to base64 for embedding in HTML
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    plt.close()  # Important: close the figure to free memory

    context = {'graphic': graphic}

    return render(request, 'plot_example.html', context)


def stock_chart(request):
    # Get your stock data
    data = get_data(request, inclusion=True)
    
    if data.get('success'):
        # Create sample data for demonstration
        dates = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
        prices = [150.0, 152.5, 148.0, 155.0, data['close_price']]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(dates, prices, marker='o', linewidth=2)
        ax.set_title(f'{data["symbol"]} Stock Price')
        ax.set_ylabel('Price ($)')
        ax.grid(True, alpha=0.3)
        
        # Save to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        
        graphic = base64.b64encode(image_png).decode('utf-8')
        plt.close()
        
        context = {'graphic': graphic, 'symbol': data['symbol']}
    else:
        context = {'error': 'No stock data available'}
    
    # return render(request, 'plot_example.html', context)


def get_data(request, inclusion=True):
    """simple polygon pull"""
    data = {}
    api_key = os.environ.get('STOCK_API_KEY', '')
    # api_key = 'buttfarts'
    symbol = 'AAPL'

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'
    # print(url)

    response = requests.get(url, timeout=10)
    data = response.json()

    # run with the backup stock.json file if the api call doesn't work
    if 'Information' in data:
        json_file = os.path.join(settings.BASE_DIR, 'stock.json')
        try:
            with open(json_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                # print('file pulled successfully')
        except FileNotFoundError:
            data = {'error': 'file not found, url not run'}
            # print('file not pulled')

    meta_data = data.get('Meta Data', {})
    symbol = meta_data.get('2. Symbol', 'Unknown')
    time_series = data.get('Time Series (Daily)', {})
    today = next(iter(time_series))
    latest_data = time_series[today]
    open_price = float(latest_data.get('1. open', 0))
    close_price = float(latest_data.get('4. close', 0))
    high_price = float(latest_data.get('2. high', 0))
    low_price = float(latest_data.get('3. low', 0))
    volume = float(latest_data.get('5. volume', 0))

    context = {
        'symbol': symbol,
        'date': today,
        'open_price': open_price,
        'close_price': close_price,
        'high_price': high_price,
        'low_price': low_price,
        'volume': volume,
        # 'data': data,
        'success': True,
    }

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
                return redirect('dashboard')

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
    return render(request, 'account.html', {'form': AccountForm()})


class AccountListView(ListView):
    model = models.Account
    context_object_name = 'stockapp_accounts'
    def get_queryset(self):
        #only for currently logged in users
        return models.Account.objects.filter(user=self.request.user)
