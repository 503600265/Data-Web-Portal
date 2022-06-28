from django.forms import ClearableFileInput
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
        fields = ()
        exclude = ('user',)

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', 'folder' )
        widgets = {
                'document': ClearableFileInput(attrs={'multiple': True, 'accept' : "image/*,.pdf"}),
                'folder': ClearableFileInput(attrs={'multiple': True,'webkitdirectory': True, 'directory': True, 'accept' : "image/*,.pdf"})
        }
