from django import forms

class SignupForm(forms.Form):
    username = forms.CharField(min_length = 3,max_length = 30)
    email = forms.EmailField()
    password = forms.CharField(min_length = 8)
    re_password = forms.CharField()
    profile_pic = forms.ImageField()

class LoginForm(forms.Form):
    username_or_email = forms.CharField(max_length = 100)
    password = forms.CharField(max_length=100)