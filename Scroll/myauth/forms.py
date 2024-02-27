from django import forms

class SignupForm(forms.Form):
    username = forms.CharField(max_length = 100)
    email = forms.EmailField()
    password = forms.PasswordInput()
    re_password = forms.PasswordInput()

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 100)
    password = forms.PasswordInput()