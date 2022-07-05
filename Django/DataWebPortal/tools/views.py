# from django.views import generic, View
# from django.views.generic import ListView, DetailView, FormView
# from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import render, redirect
from django.utils import timezone
# from django.http import Http404, HttpResponse, HttpResponseRedirect
# from django.urls import reverse
# from django.contrib import messages
# from django.template import loader
# from datetime import datetime
from .models import *
from .forms import *
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
# import pandas as pd
from django.contrib.contenttypes.models import ContentType

from django.contrib.auth.decorators import login_required, permission_required
# from django.contrib.auth import login, logout, authenticate
# from django.contrib.auth.models import User, Group
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
    convert_list = Convert.objects.filter(user=request.user).all()
    ocr_list = OCR.objects.filter(user=request.user).all()
    upload_list = zip(convert_list, ocr_list)
    context = {
        'convert_list': convert_list,
        'ocr_list': ocr_list,
        'upload_list' : upload_list
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

# def upload(request):
#     if request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
#         files = request.FILES.getlist('document')
#         if form.is_valid():
#             for f in files:
#                 file_instance = Document(document=f, user=request.user)
#                 file_instance.save()
#             # obj= form.save(commit=False)
#             # obj.user = request.user
#             # obj.save()
#             return redirect('/mydocuments')
#         if not form.is_valid():
#             return render(request=request, template_name="tools/failedupload.html")
#     else:
#         form = DocumentForm()
#     return render(request, 'tools/upload.html', {
#         'form': form
#     })

# def converts(request):
#     if request.method == 'POST':
#         form = ConvertForm(request.POST, request.FILES)
#         files = request.FILES.getlist('document')
#         if form.is_valid():
#             for f in files:
#                 file_instance = Convert(document=f, user=request.user)
#                 file_instance.save()
#             return redirect('/mydocuments')
#         if not form.is_valid():
#             return render(request=request, template_name="tools/failedupload.html")
#     else:
#         form = ConvertForm()
#     return render(request, 'tools/convert.html', {
#         'form': form
#     })

# def csv2xlsx(request):
#     if request.method == 'POST':
#         form = ConvertForm(request.POST, request.FILES)
#         if form.is_valid():
#             obj= form.save(commit=False)
#             obj.user = request.user
#             obj.save()
#             base = os.path.basename(str(obj.document))
#             file_name = os.path.splitext(base)[0]
#             convert_type = 'xlsx'
#             currentDay = datetime.datetime.now().day
#             currentMonth = datetime.datetime.now().month
#             currentYear = datetime.datetime.now().year
#             isExist = os.path.exists(media_root + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
#             if not isExist:
#               os.makedirs(media_root + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
#             convert(media_root + str(obj.document), media_root + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.'+ convert_type, output_type = convert_type )
#             converted = Convert()
#             converted.user = request.user
#             converted.document = 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.' + convert_type
#             converted.save()
#             return redirect('/mydocuments')
#         if not form.is_valid():
#             return render(request=request, template_name="tools/failedupload.html")
#     else:
#         form = ConvertForm()
#     return render(request, 'tools/convert.html', {
#         'form': form
#     })
#
# def csv2parquet(request):
#     if request.method == 'POST':
#         form = ConvertForm(request.POST, request.FILES)
#         if form.is_valid():
#             obj= form.save(commit=False)
#             obj.user = request.user
#             obj.save()
#             base = os.path.basename(str(obj.document))
#             file_name = os.path.splitext(base)[0]
#             convert_type = 'parquet'
#             currentDay = datetime.datetime.now().day
#             currentMonth = datetime.datetime.now().month
#             currentYear = datetime.datetime.now().year
#             isExist = os.path.exists(media_root + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
#             if not isExist:
#               os.makedirs(media_root + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
#             convert(media_root + str(obj.document), media_root + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.'+ convert_type, output_type = convert_type )
#             converted = Convert()
#             converted.user = request.user
#             converted.document = 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.' + convert_type
#             converted.save()
#             return redirect('/mydocuments')
#         if not form.is_valid():
#             return render(request=request, template_name="tools/failedupload.html")
#     else:
#         form = ConvertForm()
#     return render(request, 'tools/convert.html', {
#         'form': form
#     })
#
# def parquet2csv(request):
#     if request.method == 'POST':
#         form = ConvertForm(request.POST, request.FILES)
#         if form.is_valid():
#             obj= form.save(commit=False)
#             obj.user = request.user
#             obj.save()
#             base = os.path.basename(str(obj.document))
#             file_name = os.path.splitext(base)[0]
#             convert_type = 'csv'
#             currentDay = datetime.datetime.now().day
#             currentMonth = datetime.datetime.now().month
#             currentYear = datetime.datetime.now().year
#             isExist = os.path.exists(media_root + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
#             if not isExist:
#               os.makedirs(media_root + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
#             convert(media_root + str(obj.document), media_root + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.'+ convert_type, output_type = convert_type )
#             converted = Convert()
#             converted.user = request.user
#             converted.document = 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.' + convert_type
#             converted.save()
#             return redirect('/mydocuments')
#         if not form.is_valid():
#             return render(request=request, template_name="tools/failedupload.html")
#     else:
#         form = ConvertForm()
#     return render(request, 'tools/convert.html', {
#         'form': form
#     })
#
# def xlsx2parquet(request):
#     if request.method == 'POST':
#         form = ConvertForm(request.POST, request.FILES)
#         if form.is_valid():
#             obj= form.save(commit=False)
#             obj.user = request.user
#             obj.save()
#             base = os.path.basename(str(obj.document))
#             file_name = os.path.splitext(base)[0]
#             convert_type = 'parquet'
#             currentDay = datetime.datetime.now().day
#             currentMonth = datetime.datetime.now().month
#             currentYear = datetime.datetime.now().year
#             isExist = os.path.exists(media_root + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
#             if not isExist:
#               os.makedirs(media_root + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
#             convert(media_root + str(obj.document), media_root + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.'+ convert_type, output_type = convert_type )
#             converted = Convert()
#             converted.user = request.user
#             converted.document = 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.' + convert_type
#             converted.save()
#             return redirect('/mydocuments')
#         if not form.is_valid():
#             return render(request=request, template_name="tools/failedupload.html")
#     else:
#         form = ConvertForm()
#     return render(request, 'tools/convert.html', {
#         'form': form
#     })
#
# def txt2csv(request):
#     if request.method == 'POST':
#         form = ConvertForm(request.POST, request.FILES)
#         if form.is_valid():
#             obj= form.save(commit=False)
#             obj.user = request.user
#             obj.save()
#             base = os.path.basename(str(obj.document))
#             file_name = os.path.splitext(base)[0]
#             convert_type = 'csv'
#             currentDay = datetime.datetime.now().day
#             currentMonth = datetime.datetime.now().month
#             currentYear = datetime.datetime.now().year
#             isExist = os.path.exists(media_root + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
#             if not isExist:
#               os.makedirs(media_root + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
#             convert(media_root + str(obj.document), media_root + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.'+ convert_type, output_type = convert_type )
#             converted = Convert()
#             converted.user = request.user
#             converted.document = 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.' + convert_type
#             converted.save()
#             return redirect('/mydocuments')
#         if not form.is_valid():
#             return render(request=request, template_name="tools/failedupload.html")
#     else:
#         form = ConvertForm()
#     return render(request, 'tools/convert.html', {
#         'form': form
#     })
#
# def txt2xlsx(request):
#     if request.method == 'POST':
#         form = ConvertForm(request.POST, request.FILES)
#         if form.is_valid():
#             obj= form.save(commit=False)
#             obj.user = request.user
#             obj.save()
#             base = os.path.basename(str(obj.document))
#             file_name = os.path.splitext(base)[0]
#             convert_type = 'xlsx'
#             currentDay = datetime.datetime.now().day
#             currentMonth = datetime.datetime.now().month
#             currentYear = datetime.datetime.now().year
#             isExist = os.path.exists(media_root + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
#             if not isExist:
#               os.makedirs(media_root + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
#             convert(media_root + str(obj.document), media_root + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.'+ convert_type, output_type = convert_type )
#             converted = Convert()
#             converted.user = request.user
#             converted.document = 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.' + convert_type
#             converted.save()
#             return redirect('/mydocuments')
#         if not form.is_valid():
#             return render(request=request, template_name="tools/failedupload.html")
#     else:
#         form = ConvertForm()
#     return render(request, 'tools/convert.html', {
#         'form': form
#     })
#
# def xls2xlsx(request):
#     if request.method == 'POST':
#         form = ConvertForm(request.POST, request.FILES)
#         if form.is_valid():
#             obj= form.save(commit=False)
#             obj.user = request.user
#             obj.save()
#             base = os.path.basename(str(obj.document))
#             file_name = os.path.splitext(base)[0]
#             convert_type = 'xlsx'
#             currentDay = datetime.datetime.now().day
#             currentMonth = datetime.datetime.now().month
#             currentYear = datetime.datetime.now().year
#             isExist = os.path.exists(media_root + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
#             if not isExist:
#               os.makedirs(media_root + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
#             convert(media_root + str(obj.document), media_root + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.'+ convert_type, output_type = convert_type )
#             converted = Convert()
#             converted.user = request.user
#             converted.document = 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.' + convert_type
#             converted.save()
#             return redirect('/mydocuments')
#         if not form.is_valid():
#             return render(request=request, template_name="tools/failedupload.html")
#     else:
#         form = ConvertForm()
#     return render(request, 'tools/convert.html', {
#         'form': form
#     })
#
# def json2csv(request):
#     if request.method == 'POST':
#         form = ConvertForm(request.POST, request.FILES)
#         if form.is_valid():
#             obj= form.save(commit=False)
#             obj.user = request.user
#             obj.save()
#             base = os.path.basename(str(obj.document))
#             file_name = os.path.splitext(base)[0]
#             convert_type = 'csv'
#             currentDay = datetime.datetime.now().day
#             currentMonth = datetime.datetime.now().month
#             currentYear = datetime.datetime.now().year
#             isExist = os.path.exists(media_root + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
#             if not isExist:
#               os.makedirs(media_root + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
#             convert(media_root + str(obj.document), media_root + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.'+ convert_type, output_type = convert_type )
#             converted = Convert()
#             converted.user = request.user
#             converted.document = 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.' + convert_type
#             converted.save()
#             return redirect('/mydocuments')
#         if not form.is_valid():
#             return render(request=request, template_name="tools/failedupload.html")
#     else:
#         form = ConvertForm()
#     return render(request, 'tools/convert.html', {
#         'form': form
#     })
#
# def json2xlsx(request):
#     if request.method == 'POST':
#         form = ConvertForm(request.POST, request.FILES)
#         if form.is_valid():
#             obj= form.save(commit=False)
#             obj.user = request.user
#             obj.save()
#             base = os.path.basename(str(obj.document))
#             file_name = os.path.splitext(base)[0]
#             convert_type = 'xlsx'
#             currentDay = datetime.datetime.now().day
#             currentMonth = datetime.datetime.now().month
#             currentYear = datetime.datetime.now().year
#             isExist = os.path.exists(media_root + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
#             if not isExist:
#               os.makedirs(media_root + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
#             convert(media_root + str(obj.document), media_root + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.'+ convert_type, output_type = convert_type )
#             converted = Convert()
#             converted.user = request.user
#             converted.document = 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.' + convert_type
#             converted.save()
#             return redirect('/mydocuments')
#         if not form.is_valid():
#             return render(request=request, template_name="tools/failedupload.html")
#     else:
#         form = ConvertForm()
#     return render(request, 'tools/convert.html', {
#         'form': form
#     })
media_root = 'H:/Gitlab Repo/bw-cs-web-portal/Django/DataWebPortal/media/'

def log_addition(request, object, message):
    """
    Log that an object has been successfully added.
    The default implementation creates an admin LogEntry object.
    """
    return LogEntry.objects.log_action(
        user_id=request.user.pk,
        content_type_id= ContentType.objects.get_for_model(type(object)).pk,
        object_id=object.pk,
        object_repr=str(object),
        action_flag=ADDITION,
        change_message=message,
    )
@login_required
def convert(request):
    output_format = request.POST.get('output', False) #get the output from drop down list
    if request.method == 'POST':
        form = ConvertForm(request.POST, request.FILES)
        files = request.FILES.getlist('document') #get the list of files
        if form.is_valid():
            for f in files:
                obj = Convert(document=f, user=request.user) #create a instance for every file uploaded and link with its user
                obj.save()
                base = os.path.basename(str(obj.document))
                file_name = os.path.splitext(base)[0] #get the file name of the file that is uploaded
                currentDay = datetime.datetime.now().day
                currentMonth = datetime.datetime.now().month
                currentYear = datetime.datetime.now().year
                isExist = os.path.exists(media_root + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/') #check if converted folder exist, create it if doesn't
                if not isExist:
                    os.makedirs(media_root + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
                convert_document(media_root + str(obj.document), media_root + 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.'+ output_format, output_type = output_format ) #call convert_document function to convert a file to desired type and save it at converted folder
                # converted = Convert() #create an instance for the converted file and link it to the user with saved path
                # converted.user = request.user
                # converted.document = 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.' + output_format
                # converted.save()
                obj.converted_document = 'documents/converted/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.' + output_format
                obj.save()
                log_addition(request, obj, "a file is converted")
            return redirect('/mydocuments') #redirect to view my document after complete conversion
    else:
        form = ConvertForm()
    return render(request, 'tools/convert.html', {
        'form': form
    })

@login_required
def ocr(request):
    output_format = request.POST.get('output', False) #get the output from drop down list
    if request.method == 'POST':
        form = OCRForm(request.POST, request.FILES)
        files = request.FILES.getlist('document') #get the list of files from files that are uploaded
        folder = request.FILES.getlist('folder') #get the list of all files from the directory that is uploaded
        if form.is_valid():
            for f in files: # for every files that are uploaded from multiple files upload
                if str(f).endswith('.jpg') or str(f).endswith('.png') or str(f).endswith('.pdf'): #check if file is an image or pdf type
                    obj = OCR(document=f, user=request.user) #create a instance for every file uploaded and link with its user
                    obj.save()
                    base = os.path.basename(str(obj.document))
                    file_name = os.path.splitext(base)[0] #get the file name of the file that is uploaded
                    currentDay = datetime.datetime.now().day
                    currentMonth = datetime.datetime.now().month
                    currentYear = datetime.datetime.now().year
                    isExist = os.path.exists(media_root + 'documents/ocred/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/') #check if ocred folder exist, create it if doesn't
                    if not isExist:
                        os.makedirs(media_root + 'documents/ocred/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
                    ocr_file(media_root + str(obj.document), media_root + 'documents/ocred/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.'+ output_format, output_format ) #call ocr_file function to ocr a file to desired type and save it at ocred folder
                    # ocred = OCR()
                    # ocred.user = request.user #create an instance for the ocred file and link it to the user with saved path
                    obj.ocred_document = 'documents/ocred/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.' + output_format
                    obj.save()
                    log_addition(request, obj, "a file is ocred")
            for f in folder: # for every files that are uploaded from a directory, repeat the same process on the top.
                if str(f).endswith('.jpg') or str(f).endswith('.png') or str(f).endswith('.pdf'):
                    obj = OCR(document=f, user=request.user)
                    obj.save()
                    base = os.path.basename(str(obj.document))
                    file_name = os.path.splitext(base)[0]
                    currentDay = datetime.datetime.now().day
                    currentMonth = datetime.datetime.now().month
                    currentYear = datetime.datetime.now().year
                    isExist = os.path.exists(media_root + 'documents/ocred/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
                    if not isExist:
                        os.makedirs(media_root + 'documents/ocred/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/')
                    ocr_file(media_root + str(obj.document), media_root + 'documents/ocred/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.'+ output_format, output_format )
                    # ocred = OCR()
                    # ocred.user = request.user
                    # ocred.document = 'documents/ocred/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.' + output_format
                    # ocred.save()
                    obj.ocred_document = 'documents/ocred/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.' + output_format
                    obj.save()
                    log_addition(request, obj, "a file is ocred")
            return redirect('/mydocuments')
    else:
        form = OCRForm()
    return render(request, 'tools/ocr.html', {
        'form': form
    })
