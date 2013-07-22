from django import forms

class CreateUser(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.CharField()
    password = forms.CharField()
    firstname = forms.CharField()
    lastname = forms.CharField()
    cc_myself = forms.BooleanField(required=False)
