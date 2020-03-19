from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('champion/<name>/', views.champion, name='champion')
]