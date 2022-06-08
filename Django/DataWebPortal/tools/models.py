import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User

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


class Jobs(models.Model):
    id = models.Column(models.Integer, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobs", null=True)
    task = models.CharField(max_length=50, index=True, unique=False)
    inloc = models.CharField(max_length=120, unique=False)
    outloc = models.CharField(max_length=120, unique=False)
    start_time = models.DateTimeField('start time', auto_now_add=True)
    duration = models.Column(models.Float, unique=False)
    inloc_size = models.IntegerField(unique = False)

    def __repr__(self):
        return '<Jobs {}>'.format(self.user)


class Activity(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobs", null=True)
    time_in = models.DateTimeField('time in', auto_now_add=True)
    time_out = models.DateTimeField('time out', auto_now=True)

    def __repr__(self):
        return '<Activity {}>'.format(self.user)
