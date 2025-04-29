from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from . import models, forms

# Create your views here.
def home(request):
    '''Home page view'''
    return render(request, 'home.html')

class AccountView(View):
    '''Account view'''
    def get(self, request):
        '''get method'''
        # Check if it's the form URL
        if request.path.endswith('/form/'):
            form = forms.AccountForm()
            return render(request, 'account.html', {'form': form})
        return HttpResponse("Account view.")

    def post(self, request):
        '''post method'''
        # Check if it's the form URL
        if request.path.endswith('/form/'):
            form = forms.AccountForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponse("Account information saved.")
            return render(request, 'account.html', {'form': form})
        return HttpResponse("Account view.")

    def account_form(self, request):
        '''Handle account form input'''
        if request.method == 'POST':
            form = forms.AccountForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponse("Account information saved.")
        else:
            form = forms.AccountForm()
        return render(request, 'account.html', {'form': form})
