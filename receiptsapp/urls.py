from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('search/', views.search_receipts, name='search_receipts'),
    path('receipt/<int:receipt_id>', views.get_receipt, name='receipt'),
    path('add_receipt/', views.add_receipt, name='add_receipt'),
    path('receipts/', views.get_receipts, name='get_receipts'),
]