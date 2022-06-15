from django.urls import path, include, re_path
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.conf.urls import url
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.select_tools, name='select_tools'),
    path('convert/csv2xlsx', views.csv2xlsx, name='csv2xlsx'),
    path('convert/csv2parquet', views.csv2parquet, name='csv2parquet'),
    path('convert/parquet2csv', views.parquet2csv, name='parquet2csv'),
    path('convert/xlsx2parquet', views.xlsx2parquet, name='xlsx2parquet'),
    path('convert/txt2csv', views.txt2csv, name='txt2csv'),
    path('convert/txt2xlsx', views.txt2xlsx, name='txt2xlsx'),
    path('convert/xls2xlsx', views.xls2xlsx, name='xls2xlsx'),
    path('convert/json2csv', views.json2csv, name='json2csv'),
    path('convert/json2xlsx', views.json2xlsx, name='json2xlsx'),
    path('convert/', views.upload, name='convert'),
    path('ocr/', views.upload, name='ocr'),
    path('upload/', views.upload, name='upload'),



    # path('<int:job_id>/', views.detail, name='detail'),
    # path('delete/<id>', views.delete, name='delete'),
    # path('edit/<id>', views.edit, name='edit'),

]
