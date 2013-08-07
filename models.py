from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from django.contrib.auth.models import User

class CreateUser(forms.Form):
    username = forms.CharField(max_length=80, label = "User name",required = True)
    email = forms.EmailField(max_length=80, label = "Email")
    password = forms.CharField(widget=forms.PasswordInput(),label = "Password",required = True)
    firstname = forms.CharField(label = "First name")
    lastname = forms.CharField(label = "Last name")
    admin = forms.CharField(widget=forms.PasswordInput(), label = "Password for Admin Status", required = False)

      
    def __init__(self, *args, **kwargs):
      super(CreateUser, self).__init__(*args, **kwargs)
      self.helper = FormHelper()
      self.helper.form_id = 'id-exampleForm'
      self.helper.form_class = 'blueForms'
      self.helper.form_method = 'post'
      self.helper.form_style = 'default'
      self.helper.add_input(Submit('submit', 'Submit'))
     
    
class LoginUser(forms.Form):
    username = forms.CharField(
      label = "Username",
      max_length = 80,
      required = True)
    password = forms.CharField(
      widget=forms.PasswordInput(),
      label = "Password",
      max_length = 80,
      required = True)
    
    def __init__(self, *args, **kwargs):
        super(LoginUser, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
           Fieldset(
              'Login',
              'username',
              'password',
              ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
              )
        ))

        
    

