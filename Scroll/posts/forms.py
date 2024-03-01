from django import forms
# from .models import Post

class PostForm(forms.Form):
    post_file = forms.FileField()
    post_bio = forms.Textarea()
    post_type = forms.CharField()