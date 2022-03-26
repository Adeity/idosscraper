from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('connections/home_to_school/', views.home_to_school, name='connections_home_to_school'),
]
