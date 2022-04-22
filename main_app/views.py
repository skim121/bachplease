from django.shortcuts import render, get_object_or_404, redirect
from django.views import View 
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse 
from django.contrib.auth.models import User
from .models import Event, City, Tag, Schedule, DayEvent
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator 
# from django.db.models import Q
# import django_filters 

class Home(TemplateView): 
    template_name = "home.html"

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

class AustinList(TemplateView): 
    template_name = "citylist.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = Event.objects.filter(city=1)
        context["header"] = f"Austin"
        return context

class NashvilleList(TemplateView): 
    template_name = "citylist.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = Event.objects.filter(city=2)
        context["header"] = f"Nashville"
        return context

class MiamiList(TemplateView): 
    template_name = "citylist.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = Event.objects.filter(city=3)
        context["header"] = f"Miami"
        return context


def EventDetail(request,id): 
    event = get_object_or_404(Event, id=id)
    events = Event.objects.filter(user=request.user.id)
    is_fav = False
    if event in events:
        is_fav = True
    return render(request, 'event_detail.html', {'event': event, 'is_fav': is_fav})

def profile(request, id): 
    user = User.objects.get(id=id)
    events = Event.objects.filter(user=request.user)
    schedules = Schedule.objects.filter(user=request.user)
    return render(request, 'profile.html', {'user': user, 'events': events, 'schedules': schedules, id: request.user.id})

def fav_add(request, id): 
    event = get_object_or_404(Event, id=id)
    if event.user.filter(id=request.user.id).exists():
        event.user.remove(request.user)
    else: 
        event.user.add(request.user)
    return HttpResponseRedirect('/event/'+str(event.id))

def schedule(request, id):
    schedule = Schedule.objects.filter(id=id)
    return render(request, 'schedule.html', {'schedule': schedule, 'id':schedule.id})

def ScheduleDetail(request,id): 
    schedule = get_object_or_404(Schedule, id=id)
    events = Event.objects.filter(user=request.user, city=schedule.city)
    return render(request, 'schedule_detail.html', {'schedule': schedule, 'events': events})

@method_decorator(login_required, name='dispatch')
class ScheduleCreate(CreateView):
    model = Schedule
    fields= ['name','date_in','date_out','numdays', 'city']
    template_name = 'schedule_create.html'
    def form_valid(self, form): 
        self.object = form.save(commit=False)
        self.object.user= self.request.user
        self.object.save()
        return HttpResponseRedirect('/user/'+str(self.object.user.id))


@method_decorator(login_required, name='dispatch')
class ScheduleDelete(DeleteView): 
    model = Schedule
    template_name = "schedule_delete_confirm.html"
    def get_success_url(self):
        return reverse('profile', kwargs={'id': self.object.user.id}) 

