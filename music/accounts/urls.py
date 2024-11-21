from django.contrib import admin
from django.urls import path
from .views import login, callback

urlpatterns = [
    path('', login, name='login'),
    path('callback/', callback),
]