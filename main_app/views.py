from django.shortcuts import render, get_object_or_404, redirect
from django.views import View 
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required


class Home(TemplateView): 
    template_name = "home.html"
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

