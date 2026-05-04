from django import forms
from django.conf import settings
from django.forms import ModelForm
from allauth.account.forms import LoginForm, SignupForm
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

from .models import Delivery_Address_Details



class CustomSignupForm(SignupForm):
    # Add captcha to signup to block automated account creation attempts.
    if not settings.DEBUG:
        # Only enforce reCAPTCHA in production-like environments.
        captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
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


class CustomLoginForm(LoginForm):
    # Add captcha to login to reduce credential stuffing/bot sign-in attempts.
    if not settings.DEBUG:
        # Only enforce reCAPTCHA in production-like environments.
        captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

class Delivery_Information(ModelForm):
    
    notes = forms.CharField(max_length=200, required=False)


    class Meta:
        model = Delivery_Address_Details
        fields = ['name', 'last_name', 'phone_number', 'city_town', 
                    'street_name', 'building_appartment', 'delivery_details']
