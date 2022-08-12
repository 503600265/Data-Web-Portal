import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User
import os
from django.core.exceptions import ValidationError


def validate_file_extension_convert(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.csv','.xlsx','.xls','.txt','.parquet','.json']
    if not ext in valid_extensions:
        raise ValidationError(u'Wrong File Input, choose csv, xlsx, parquet, txt, xls, or json')

def validate_file_extension_ocr(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.png','.jpg','.jpeg','.gif','.pdf']
    if not ext in valid_extensions:
        raise ValidationError(u'Wrong File Input, choose image or pdf')

class Convert(models.Model):
    description = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="converted_document", null=True)
    document = models.FileField(upload_to='documents/uploaded/%Y/%m/%d/', blank=True, null=True, validators=[validate_file_extension_convert])
    converted_document = models.FileField(upload_to=None, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def is_uploaded(self):
        return self.document
    def is_converted(self):
        return self.converted_document
    
class OCR(models.Model):
    description = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ocred_document", null=True)
    document = models.FileField(upload_to='documents/uploaded/%Y/%m/%d/', blank=True, null=True, validators=[validate_file_extension_ocr])
    ocred_document = models.FileField(upload_to=None, blank=True, null=True)
    folder = models.FileField(upload_to='documents/uploaded/%Y/%m/%d/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def is_uploaded(self):
        return self.document
    def is_ocred(self):
        return self.ocred_document
    def clean(self):
        if not (self.document or self.folder):
            raise ValidationError("You must select either file or folder")

class Job(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobs", null=True)
    task = models.CharField(max_length=50, unique=False)
    inloc = models.CharField(max_length=120, unique=False)
    outloc = models.CharField(max_length=120, unique=False)
    start_time = models.DateTimeField('start time', auto_now_add=True)
    duration = models.FloatField(unique=False)
    inloc_size = models.IntegerField(unique = False)

    def __repr__(self):
        return '<Jobs {}>'.format(self.user)


class Activity(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="activity", null=True)
    time_in = models.DateTimeField('time in', auto_now_add=True)
    time_out = models.DateTimeField('time out', auto_now=True)

    def __repr__(self):
        return '<Activity {}>'.format(self.user)
