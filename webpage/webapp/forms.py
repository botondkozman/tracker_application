from django import forms

class ImageForm(forms.Form):
    user_image = forms.FileField()