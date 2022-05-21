from turtle import numinput
from django import forms
# users model file
from .models import *
# user model import 
from users.models import *
from datetime import datetime
from allauth.account.forms import SignupForm
from phonenumber_field.modelfields import PhoneNumberField



class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')

    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save() 

        # Add your own processing here.

        # You must return the original result.
        return user
        
class Delivery_Information(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput() ,max_length=30, required=True)
    last_name = forms.CharField(widget=forms.TextInput(),max_length=40,required=True)
    phone = forms.IntegerField(widget=forms.TextInput())
    city_town = forms.CharField(max_length=200)
    street = forms.CharField(max_length=200)
    building_appartement = forms.CharField(max_length=200)
    additional_information = forms.CharField(max_length=255)
    note = forms.CharField(max_length=200)
    