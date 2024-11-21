from django.contrib import admin
from django.urls import path
from .views import homepage, search, quiz, save_result, user_profile

urlpatterns = [
    path('', homepage, name='home'),
    path('search/', search, name='partial_search'),
    path('quiz/<str:artist_id>/',quiz, name='quiz'),
    path('save_result/<str:artist_id>/', save_result, name='save_result'),
    path('profile/', user_profile, name='profile'),
]