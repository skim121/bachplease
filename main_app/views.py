from django.shortcuts import render, get_object_or_404, redirect
from django.views import View 
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse 

class Home(TemplateView): 
    template_name = "home.html"

# Create your views here.
