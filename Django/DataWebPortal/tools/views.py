
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

# Create your views here.
@login_required
def jobs(request):
    jobs_list = Jobs.objects.filter().all()
    context = {
        'jobs_list': jobs_list
    }
    return render(request, 'tools/myjobs.html', context)
    
@login_required
def document(request):
    documents_list = Document.objects.filter().all()
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
            form.save()
            return redirect('/')
    else:
        form = DocumentForm()
    return render(request, 'tools/upload.html', {
        'form': form
    })

# @login_required
# def edit(request, id):
#     labeling = get_object_or_404(Labeling, id=id)
#     context = dict( backend_form = LabelingForm())
#     if request.method == 'POST':
#         form = LabelingForm(request.POST, request.FILES, instance=labeling)
#         if form.is_valid():
#             labeling.publishDate=timezone.datetime.now()
#             labeling.save()
#             return redirect('/tools')
#     return render(request, 'tools/edit.html', context)
#
# @login_required
# def delete(request, id):
#     # dictionary for initial data with
#     # field names as keys
#     context = dict( backend_form = LabelingForm())
#     obj = get_object_or_404(Labeling, id = id)


    # fetch the object related to passed id



    # if request.method =="POST":
    #     # delete object
    #     obj.delete()
    #     # after deleting redirect to
    #     # home page
    #     return redirect('/tools')
    # return render(request, "tools/index.html", context)
