from django.urls import path, include, re_path
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.conf.urls import url
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.select_tools, name='select_tools'),
    path('convert/', views.convert, name='convert'),
    path('ocr/', views.ocr, name='ocr'),
]
