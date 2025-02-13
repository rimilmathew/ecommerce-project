from django import forms
from django.contrib.auth.models import User


class Userform(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)
    class Meta:
        model=User
        fields=['username','password','confirm_password','email','first_name','last_name']