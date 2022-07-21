from django import forms
# users model file
from .models import *
# user model import 
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from users.models import *
from datetime import datetime
from allauth.account.forms import SignupForm
from django.core.validators import MaxValueValidator
# from phonenumber_field.modelfields import PhoneNumberField



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
        
# class Delivery_Information(forms.Form):
#     first_name = forms.CharField(widget=forms.TextInput() ,max_length=30, required=True)
#     last_name = forms.CharField(widget=forms.TextInput(),max_length=40,required=True)
#     phone = forms.IntegerField(widget=forms.TextInput(), required=True,validators=[MaxValueValidator(99999999)])
#     city_town = forms.CharField(max_length=200, required=True)
#     street = forms.CharField(max_length=200)
#     building_appartement = forms.CharField(max_length=200)
#     additional_information = forms.CharField(max_length=255, required=False)
#     note = forms.CharField(max_length=200, required=False)
    
class Delivery_Information(ModelForm):
    
    notes = forms.CharField(max_length=200, required=False)


    class Meta:
        model = Delivery_Address_Details
        fields = ['name', 'last_name', 'phone_number', 'city_town', 
                    'street_name', 'building_appartment', 'delivery_details']
