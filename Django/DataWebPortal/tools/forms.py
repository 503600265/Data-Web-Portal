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

class ConvertForm(forms.ModelForm):
    class Meta:
        model = Convert
        fields = ('description', 'document')
        widgets = {
                'document': ClearableFileInput(attrs={'accept' : "text/csv, text/plain, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel, application/json, .parquet, "}),
        }

class OCRForm(forms.ModelForm):
    class Meta:
        model = OCR
        fields = ('description', 'document', 'folder' )
        widgets = {
                'document': ClearableFileInput(attrs={'multiple': True, 'accept' : "image/*,.pdf"}),
                'folder': ClearableFileInput(attrs={'multiple': True,'webkitdirectory': True, 'directory': True, 'accept' : "image/*,.pdf"})
        }
