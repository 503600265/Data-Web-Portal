
from django.views import generic, View
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.template import loader

from .models import Jobs, Activity
from .forms import *
import pandas as pd
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
import sys
sys.path.insert(0, 'H:\Gitlab Repo\bw-cs-web-portal\Django\DataWebPortal\tools\data_processes')
from .data_processes.convert_data import *
# Create your views here.
@login_required
def jobs(request):
    jobs_list = Jobs.objects.filter(user=request.user).all()
    context = {
        'jobs_list': jobs_list
    }
    return render(request, 'tools/myjobs.html', context)

@login_required
def document(request):
    documents_list = Document.objects.filter(user=request.user).all()
    context = {
        'documents_list': documents_list
    }
    return render(request, 'tools/mydocuments.html', context)

@login_required
def select_tools(request):
    return render(request, 'tools/select_tools.html')
# @login_required
# def detail(request, labeling_id):
#     labeling = get_object_or_404(Labeling, pk=labeling_id)
#     return render(request, 'tools/detail.html', {'labeling': labeling})

# @login_required
def about(request):
    return render(request, 'tools/about.html')

@login_required
def upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            obj= form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('/')
        if not form.is_valid():
            return render(request=request, template_name="tools/failedupload.html")
    else:
        form = DocumentForm()
    return render(request, 'tools/upload.html', {
        'form': form
    })

def convert(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            obj= form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('/')
        if not form.is_valid():
            return render(request=request, template_name="tools/failedupload.html")
    else:
        form = DocumentForm()
    return render(request, 'tools/convert.html')
