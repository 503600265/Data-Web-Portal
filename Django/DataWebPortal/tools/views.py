
from django.views import generic, View
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.template import loader
from datetime import datetime
from .models import Jobs, Activity
from .forms import *
import pandas as pd
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
import os
import sys
sys.path.insert(0, 'H:\Gitlab Repo\bw-cs-web-portal\Django\DataWebPortal\tools\data_processes')
from .data_processes.convert_data import *
from .data_processes.ocr_docs import *

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

# @login_required
# def upload(request):
#     if request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             obj= form.save(commit=False)
#             obj.user = request.user
#             obj.save()
#             return redirect('/mydocuments')
#         if not form.is_valid():
#             return render(request=request, template_name="tools/failedupload.html")
#     else:
#         form = DocumentForm()
#     return render(request, 'tools/upload.html', {
#         'form': form
#     })

# def convert(request, document_dir, download_dir, type):
#     document = Document.objects.filter(document= document_dir).all()
#     convert_document(document.document, download_dir, type)
#     return render(request, 'tools/convert.html')

# def convert(request):
#     if request.method == "POST":
#         # creating random folder name for each user
#         res = ''.join(random.choice(string.ascii_lowercase) for x in range(10))
#         path_to_upload = os.path.join('./convertor/static/uploaded_files/jpg2pdf', str(res))
#         os.makedirs(path_to_upload)
#         files = request.FILES
#         files_list = []
#         for file in files.getlist('files'):
#             files_list.append(file)
#
#         a4inpt = (img2pdf.mm_to_pt(210), img2pdf.mm_to_pt(297))
#         layout_fun = img2pdf.get_layout_fun(a4inpt)
#         with open(path_to_upload + "/sample.pdf", "wb") as f:
#             f.write(img2pdf.convert(files_list, layout_fun=layout_fun))
#         os.rename(path_to_upload + "/sample.pdf", path_to_upload + "/sample.txt")
#         return render(request, 'jpgtopdf.html', {'url': str(res)})
#     return render(request, 'jpgtopdf.html')
# def csv2xlsx(request):
#     if request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             obj= form.save(commit=False)
#             obj.user = request.user
#             obj.save()
#             file_name, file_extension = os.path.splitext(obj.document)
#             csv_to_xlsx(obj.document, file_name + ".xlsx", "xlsx" )
#             converted = Document()
#             converted.user = request.user
#             converted.document = file_name + ".xlsx"
#             return redirect('/mydocuments')
#         if not form.is_valid():
#             return render(request=request, template_name="tools/failedupload.html")
#     else:
#         form = DocumentForm()
#     return render(request, 'tools/upload.html', {
#         'form': form
#     })

def upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            obj= form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('/mydocuments')
        if not form.is_valid():
            return render(request=request, template_name="tools/failedupload.html")
    else:
        form = DocumentForm()
    return render(request, 'tools/upload.html', {
        'form': form
    })

def converts(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            obj= form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('/mydocuments')
        if not form.is_valid():
            return render(request=request, template_name="tools/failedupload.html")
    else:
        form = DocumentForm()
    return render(request, 'tools/convert.html', {
        'form': form
    })

def csv2xlsx(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            obj= form.save(commit=False)
            obj.user = request.user
            obj.save()
            base = os.path.basename(str(obj.document))
            file_name = os.path.splitext(base)[0]
            convert_type = 'xlsx'
            currentDay = datetime.datetime.now().day
            currentMonth = datetime.datetime.now().month
            currentYear = datetime.datetime.now().year
            isExist = os.path.exists('H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
            if not isExist:
              os.makedirs('H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
            convert('H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + str(obj.document), 'H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.'+ convert_type, output_type = convert_type )
            converted = Document()
            converted.user = request.user
            converted.document = 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.' + convert_type
            converted.save()
            return redirect('/mydocuments')
        if not form.is_valid():
            return render(request=request, template_name="tools/failedupload.html")
    else:
        form = DocumentForm()
    return render(request, 'tools/convert.html', {
        'form': form
    })

def csv2parquet(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            obj= form.save(commit=False)
            obj.user = request.user
            obj.save()
            base = os.path.basename(str(obj.document))
            file_name = os.path.splitext(base)[0]
            convert_type = 'parquet'
            currentDay = datetime.datetime.now().day
            currentMonth = datetime.datetime.now().month
            currentYear = datetime.datetime.now().year
            isExist = os.path.exists('H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
            if not isExist:
              os.makedirs('H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
            convert('H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + str(obj.document), 'H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.'+ convert_type, output_type = convert_type )
            converted = Document()
            converted.user = request.user
            converted.document = 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.' + convert_type
            converted.save()
            return redirect('/mydocuments')
        if not form.is_valid():
            return render(request=request, template_name="tools/failedupload.html")
    else:
        form = DocumentForm()
    return render(request, 'tools/convert.html', {
        'form': form
    })

def parquet2csv(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            obj= form.save(commit=False)
            obj.user = request.user
            obj.save()
            base = os.path.basename(str(obj.document))
            file_name = os.path.splitext(base)[0]
            convert_type = 'csv'
            currentDay = datetime.datetime.now().day
            currentMonth = datetime.datetime.now().month
            currentYear = datetime.datetime.now().year
            isExist = os.path.exists('H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
            if not isExist:
              os.makedirs('H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
            convert('H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + str(obj.document), 'H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.'+ convert_type, output_type = convert_type )
            converted = Document()
            converted.user = request.user
            converted.document = 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.' + convert_type
            converted.save()
            return redirect('/mydocuments')
        if not form.is_valid():
            return render(request=request, template_name="tools/failedupload.html")
    else:
        form = DocumentForm()
    return render(request, 'tools/convert.html', {
        'form': form
    })

def xlsx2parquet(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            obj= form.save(commit=False)
            obj.user = request.user
            obj.save()
            base = os.path.basename(str(obj.document))
            file_name = os.path.splitext(base)[0]
            convert_type = 'parquet'
            currentDay = datetime.datetime.now().day
            currentMonth = datetime.datetime.now().month
            currentYear = datetime.datetime.now().year
            isExist = os.path.exists('H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
            if not isExist:
              os.makedirs('H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
            convert('H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + str(obj.document), 'H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.'+ convert_type, output_type = convert_type )
            converted = Document()
            converted.user = request.user
            converted.document = 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.' + convert_type
            converted.save()
            return redirect('/mydocuments')
        if not form.is_valid():
            return render(request=request, template_name="tools/failedupload.html")
    else:
        form = DocumentForm()
    return render(request, 'tools/convert.html', {
        'form': form
    })

def txt2csv(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            obj= form.save(commit=False)
            obj.user = request.user
            obj.save()
            base = os.path.basename(str(obj.document))
            file_name = os.path.splitext(base)[0]
            convert_type = 'csv'
            currentDay = datetime.datetime.now().day
            currentMonth = datetime.datetime.now().month
            currentYear = datetime.datetime.now().year
            isExist = os.path.exists('H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
            if not isExist:
              os.makedirs('H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
            convert('H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + str(obj.document), 'H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.'+ convert_type, output_type = convert_type )
            converted = Document()
            converted.user = request.user
            converted.document = 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.' + convert_type
            converted.save()
            return redirect('/mydocuments')
        if not form.is_valid():
            return render(request=request, template_name="tools/failedupload.html")
    else:
        form = DocumentForm()
    return render(request, 'tools/convert.html', {
        'form': form
    })

def txt2xlsx(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            obj= form.save(commit=False)
            obj.user = request.user
            obj.save()
            base = os.path.basename(str(obj.document))
            file_name = os.path.splitext(base)[0]
            convert_type = 'xlsx'
            currentDay = datetime.datetime.now().day
            currentMonth = datetime.datetime.now().month
            currentYear = datetime.datetime.now().year
            isExist = os.path.exists('H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
            if not isExist:
              os.makedirs('H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
            convert('H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + str(obj.document), 'H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.'+ convert_type, output_type = convert_type )
            converted = Document()
            converted.user = request.user
            converted.document = 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.' + convert_type
            converted.save()
            return redirect('/mydocuments')
        if not form.is_valid():
            return render(request=request, template_name="tools/failedupload.html")
    else:
        form = DocumentForm()
    return render(request, 'tools/convert.html', {
        'form': form
    })

def xls2xlsx(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            obj= form.save(commit=False)
            obj.user = request.user
            obj.save()
            base = os.path.basename(str(obj.document))
            file_name = os.path.splitext(base)[0]
            convert_type = 'xlsx'
            currentDay = datetime.datetime.now().day
            currentMonth = datetime.datetime.now().month
            currentYear = datetime.datetime.now().year
            isExist = os.path.exists('H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
            if not isExist:
              os.makedirs('H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
            convert('H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + str(obj.document), 'H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.'+ convert_type, output_type = convert_type )
            converted = Document()
            converted.user = request.user
            converted.document = 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.' + convert_type
            converted.save()
            return redirect('/mydocuments')
        if not form.is_valid():
            return render(request=request, template_name="tools/failedupload.html")
    else:
        form = DocumentForm()
    return render(request, 'tools/convert.html', {
        'form': form
    })

def json2csv(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            obj= form.save(commit=False)
            obj.user = request.user
            obj.save()
            base = os.path.basename(str(obj.document))
            file_name = os.path.splitext(base)[0]
            convert_type = 'csv'
            currentDay = datetime.datetime.now().day
            currentMonth = datetime.datetime.now().month
            currentYear = datetime.datetime.now().year
            isExist = os.path.exists('H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
            if not isExist:
              os.makedirs('H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
            convert('H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + str(obj.document), 'H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.'+ convert_type, output_type = convert_type )
            converted = Document()
            converted.user = request.user
            converted.document = 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.' + convert_type
            converted.save()
            return redirect('/mydocuments')
        if not form.is_valid():
            return render(request=request, template_name="tools/failedupload.html")
    else:
        form = DocumentForm()
    return render(request, 'tools/convert.html', {
        'form': form
    })

def json2xlsx(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            obj= form.save(commit=False)
            obj.user = request.user
            obj.save()
            base = os.path.basename(str(obj.document))
            file_name = os.path.splitext(base)[0]
            convert_type = 'xlsx'
            currentDay = datetime.datetime.now().day
            currentMonth = datetime.datetime.now().month
            currentYear = datetime.datetime.now().year
            isExist = os.path.exists('H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
            if not isExist:
              os.makedirs('H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
            convert('H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + str(obj.document), 'H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.'+ convert_type, output_type = convert_type )
            converted = Document()
            converted.user = request.user
            converted.document = 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.' + convert_type
            converted.save()
            return redirect('/mydocuments')
        if not form.is_valid():
            return render(request=request, template_name="tools/failedupload.html")
    else:
        form = DocumentForm()
    return render(request, 'tools/convert.html', {
        'form': form
    })

def ocr(request):
    output_format = request.POST.get('output', False)
    print(output_format)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            obj= form.save(commit=False)
            obj.user = request.user
            obj.save()
            base = os.path.basename(str(obj.document))
            file_name = os.path.splitext(base)[0]
            currentDay = datetime.datetime.now().day
            currentMonth = datetime.datetime.now().month
            currentYear = datetime.datetime.now().year
            isExist = os.path.exists('H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + 'documents/ocred/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
            if not isExist:
                 os.makedirs('H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + 'documents/ocred/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
            ocr_file('H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + str(obj.document), 'H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/' + 'documents/ocred/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.'+ output_format, output_format )
            ocred = Document()
            ocred.user = request.user
            ocred.document = 'documents/ocred/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.' + output_format
            ocred.save()
            return redirect('/mydocuments')
        if not form.is_valid():
            return render(request=request, template_name="tools/failedupload.html")
    else:
        form = DocumentForm()
    return render(request, 'tools/ocr.html', {
        'form': form
    })
