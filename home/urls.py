from django.urls import path
from . import views

urlpatterns =[
    path('', views.home, name='home'),
    # path('process_upload', views.process_upload, name='process_upload'),
]