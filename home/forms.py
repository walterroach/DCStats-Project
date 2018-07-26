#home.forms
import pytz
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from stats.models import Pilot, UserProfile


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, help_text='Required')
    last_name = forms.CharField(max_length=30, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name')

class UserForm(ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email']

class PilotProfileForm(ModelForm):
	class Meta:
		model = Pilot
		fields = ['callsign']

class UserProfileForm(ModelForm):
	class Meta:
		model = UserProfile
		fields = ['timezone']