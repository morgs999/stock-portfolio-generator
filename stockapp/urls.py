from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('account/', views.AccountView.as_view(), name='account'),
    path('account/form/', views.AccountView.as_view(), name='account_form'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
