import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User
import os
# from winmagic import magic
from django.core.exceptions import ValidationError

# class Users(models.Model):
#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)
#
#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)
#
#     id = models.IntegerField(primary_key=True)
#     username = models.CharField(max_length=50, unique=True)
#     email = models.CharField(max_length=50, unique=True)
#     password = models.CharField(max_length=50)
#     first = models.CharField(max_length=50)
#     last = models.CharField(max_length=50)
#
#     def __repr__(self):
#         return '<Users {}>'.format(self.username)

# def validate_mime_type_ocr(value):
#     supported_types=['application/pdf', 'image/*']
#     with magic.Magic(flags=magic.MAGIC_MIME_TYPE) as m:
#         mime_type=m.id_buffer(value.file.read(1024))
#         value.file.seek(0)
#     if mime_type not in supported_types:
#         raise ValidationError(u'Unsupported file type.')

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
    # def file_type(self):
    #     name, extension = os.path.splitext(str(self.document))
    #     input_type = extension
    #     return input_type
    # def is_uploaded(self):
    #     path = os.path.normpath(str(self.document))
    #     path_list = path.split(os.sep)
    #     if 'uploaded' in path_list:
    #         return True
    # def is_converted(self):
    #     path = os.path.normpath(str(self.document))
    #     path_list = path.split(os.sep)
    #     if 'converted' in path_list:
    #         return True
    # def is_ocred(self):
    #     path = os.path.normpath(str(self.document))
    #     path_list = path.split(os.sep)
    #     if 'ocred' in path_list:
    #         return True
    # def clean(self):
    #     if not (self.document or self.folder):
    #         raise ValidationError("You must select either file or folder")
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
    # def file_type(self):
    #     name, extension = os.path.splitext(str(self.document))
    #     input_type = file_extension
    #     return input_type
    # def is_uploaded(self):
    #     path = os.path.normpath(str(self.document))
    #     path_list = path.split(os.sep)
    #     if 'uploaded' in path_list:
    #         return True
    # def is_converted(self):
    #     path = os.path.normpath(str(self.document))
    #     path_list = path.split(os.sep)
    #     if 'converted' in path_list:
    #         return True
    # def is_ocred(self):
    #     path = os.path.normpath(str(self.document))
    #     path_list = path.split(os.sep)
    #     if 'ocred' in path_list:
    #         return True
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
