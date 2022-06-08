from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class JobsForm(forms.ModelForm):

    class Meta:
        model = Jobs
        fields = ('task', 'inloc','outloc')
        exclude = ('user',)

class ActivityForm(forms.ModelForm):

    class Meta:
        model = Activity
        fields = ('time_in', 'time_out')
        exclude = ('user',)
