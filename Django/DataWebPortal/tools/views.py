from django.shortcuts import render, redirect
from django.utils import timezone
from .models import *
from .forms import *
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
import os
import sys
sys.path.insert(0, '/home/xxx@xxxx.com/bw-cs-web-portal/Django/DataWebPortal/tools/data_processes')
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
def about(request):
    return render(request, 'tools/about.html')

media_root = '/home/xxx@xxxxx.com/bw-cs-web-portal/Django/DataWebPortal/media/'

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
                    obj.ocred_document = 'documents/ocred/' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay) + '/' + file_name + '.' + output_format
                    obj.save()
                    log_addition(request, obj, "a file is ocred")
            return redirect('/mydocuments')
    else:
        form = OCRForm()
    return render(request, 'tools/ocr.html', {
        'form': form
    })
