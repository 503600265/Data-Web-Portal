from django.urls import path, include, re_path
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
# from django.conf.urls import url

from . import views

urlpatterns = [
    path('home/', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('admin/', admin.site.urls),
    # path('<int:job_id>/', views.detail, name='detail'),
    # path('delete/<id>', views.delete, name='delete'),
    # path('edit/<id>', views.edit, name='edit'),
    path('upload/', views.upload, name='upload'),
]
