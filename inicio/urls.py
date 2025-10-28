
from django.urls import path
from . import views
urlpatterns = [
  path('', views.index),
  path('inicio', views.index,name='inicio')
]