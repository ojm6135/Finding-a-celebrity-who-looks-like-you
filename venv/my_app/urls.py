from django.contrib import admin
from django.urls import path
from my_app import views


urlpatterns = [
    path('', views.index),
    path('search/', views.search),
    path('result/', views.show_result),
]
