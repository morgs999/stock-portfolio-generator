from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('account/', views.AccountView.as_view(), name='account'),
    path('account/form/', views.AccountView.as_view(), name='account_form'),
]
