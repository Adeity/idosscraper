from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world!")

def home_to_school(request):
    return HttpResponse("Yayayaya!!!")
