from typing import Any
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.auth.models import User

from django import forms

from django.forms.widgets import PasswordInput, TextInput


#Registration form
class CreateUserForm(UserCreationForm):
    
    class Meta:
        
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        
        # Mark email as required when registering
        self.fields['email'].required = True
    
    
    def clean_email(self): #Email validation
        
        email = self.cleaned_data.get('email') #Collect the email based on the fields 
        
        if User.objects.filter(email=email).exists(): #Check the email in the database with the email the user entering is exists and raise an validationerror
            
            raise forms.ValidationError('Email already exists, please try again.')
        
        if len(email) >= 350: #Check the email length
            
            raise forms.ValidationError('The email is too long, please try again.')
        
        return email #saving the email to the database after validation
    
    
    
    
    
    
# Login form

class LoginForm(AuthenticationForm):
    
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())
    
    
    
# Update form

class UpdateUserForm(forms.ModelForm):
    
    password = None
    class Meta:
        model = User
        
        fields =['username', 'email']
        exclude = ['password1', 'password2']
        
            
    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        
        # Mark email as required when registering
        self.fields['email'].required = True    
        
    
    def clean_email(self): #Email validation
        
        email = self.cleaned_data.get('email') #Collect the email based on the fields 
        
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists(): #Check the email in the database with the email the user entering is exists and raise an validation error
            #exclude(pk=self.instance.pk) excluding the email of current user, allowed to update even the email stay as the same
            raise forms.ValidationError('Email already exists, please try again.')
        
        if len(email) >= 350: #Check the email length
            
            raise forms.ValidationError('The email is too long, please try again.')
        
        return email #saving the email to the database after validation
    