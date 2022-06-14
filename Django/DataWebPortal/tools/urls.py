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
    path('convert/', views.upload, name='convert'),
    path('ocr/', views.upload, name='ocr'),
    path('upload/', views.upload, name='upload'),



    # path('<int:job_id>/', views.detail, name='detail'),
    # path('delete/<id>', views.delete, name='delete'),
    # path('edit/<id>', views.edit, name='edit'),

]
