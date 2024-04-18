from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

from .models import Receipt


class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = ['name', 'description', 'sequence_steps', 'time_to_cook', 'image', 'categories']


class ProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')