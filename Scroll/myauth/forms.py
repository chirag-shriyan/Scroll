from django import forms

class SignupForm(forms.Form):
    username = forms.CharField(max_length = 100)
    email = forms.EmailField()
    password = forms.CharField(max_length=100)
    re_password = forms.CharField(max_length=100)
    profile_pic = forms.ImageField()

class LoginForm(forms.Form):
    username_or_email = forms.CharField(max_length = 100)
    password = forms.CharField(max_length=100)