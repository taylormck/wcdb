from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class CreateUser(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.CharField()
    password = forms.CharField()
    firstname = forms.CharField()
    lastname = forms.CharField()
    cc_myself = forms.BooleanField(required=False)
    
class Login(forms.Form):
    username = forms.CharField(
      label = "Username",
      max_length = 80,
      required = True)
    password = forms.CharField(
      label = "Password",
      max_length = 80,
      required = True)
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'Submit'))
        super(Login, self).__init__(*args, **kwargs)
    

