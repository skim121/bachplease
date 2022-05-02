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
from .filters import EventFilter, CityFilter
from .forms import DayEventForm, ScheduleForm, ScheduleUpdateForm 
import folium
import os
import jsonpickle
import json
import datetime

# from django.core.exceptions import ValidationError 
# from django.db.models import Q
# import django_filters 



def Home(request): 
    tags = Tag.objects.all()
    events = Event.objects.all()
    event_filter = EventFilter(request.GET, queryset = events)
    events = event_filter.qs
    return render(request, 'home.html', {'event_filter': event_filter, 'events':events})

### FILTERS
# Filtering function from home to another page - grabs data from form on homepage and filters based on results
def FilterView(request): 
    header = request.GET['city']
    tagresults = request.GET.getlist('tag')
    cityname = City.objects.filter(id=header).values_list('name', flat=True)
    tagname = Tag.objects.filter(id__in=tagresults)
    events = Event.objects.filter(tag__in=tagname, city=header)
    city_filter = CityFilter(request.GET, queryset = events)
    events = city_filter.qs
    googleapi = os.environ.get('EASY_MAPS_GOOGLE_KEY')
    return render(request, 'citylist.html', {'header': cityname, 'tags': tagname, 'events':events, 'city_filter': city_filter, 'googleapi': googleapi})

# Pre-made search filter to Austin 
def AustinList(request): 
    events = Event.objects.filter(city=1)
    header = ["Austin"]
    city_filter = CityFilter(request.GET, queryset = events)
    events = city_filter.qs
    googleapi = os.environ.get('EASY_MAPS_GOOGLE_KEY')
    return render(request, 'citylist.html', {'city_filter': city_filter, 'events': events, 'header': header, 'googleapi': googleapi})


# Pre-made search filter to Nashville
def NashvilleList(request): 
    events = Event.objects.filter(city=2)
    header = ["Nashville"]
    city_filter = CityFilter(request.GET, queryset = events)
    events = city_filter.qs
    googleapi = os.environ.get('EASY_MAPS_GOOGLE_KEY')
    print(city_filter.filters['city'])
    return render(request, 'citylist.html', {'city_filter': city_filter, "events": events, "header": header, 'googleapi': googleapi})

# Pre-made search filter to Miami
def MiamiList(request): 
    events = Event.objects.filter(city=3)
    header = ["Miami"]
    city_filter = CityFilter(request.GET, queryset = events)
    events = city_filter.qs
    googleapi = os.environ.get('EASY_MAPS_GOOGLE_KEY')
    return render(request, 'citylist.html', {'city_filter': city_filter, "events": events, "header": header, 'googleapi': googleapi})

### EVENTS
def EventDetail(request, id): 
    event = get_object_or_404(Event, id=id)
    events = Event.objects.filter(user=request.user.id)
    is_fav = False
    if event in events:
        is_fav = True
    return render(request, 'event_detail.html', {'event': event, 'is_fav': is_fav})

### PROFILE 
# Authentication 
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

# Profile page
@login_required
def profile(request, id): 
    user = User.objects.get(id=id)
    events = Event.objects.filter(user=request.user)
    today = datetime.datetime.now() 
    schedules = Schedule.objects.filter(user=request.user)
    past = Schedule.objects.filter(user=request.user, date_in__lt=today)
    future = Schedule.objects.filter(user=request.user, date_in__gte=today)
    return render(request, 'profile.html', {'user': user, 'events': events, 'schedules': schedules, 'past': past, 'future': future, id: request.user.id})

# Add to favorites funcion
@login_required
def fav_add(request, id): 
    event = get_object_or_404(Event, id=id)
    if event.user.filter(id=request.user.id).exists():
        event.user.remove(request.user)
    else: 
        event.user.add(request.user)
    return HttpResponseRedirect('/event/'+str(event.id))

### SCHEDULES 
@login_required
def ScheduleDetail(request,id): 
    schedule = get_object_or_404(Schedule, id=id)
    print(schedule.id)
    looptimes = range(1, schedule.numdays+1)
    events = Event.objects.filter(user=request.user, city=schedule.city)
    dayevents = DayEvent.objects.filter(schedule=schedule.id)
    print(dayevents)
    return render(request, 'schedule_detail.html', {'schedule': schedule, 'events': events, 'looptimes': looptimes, 'dayevents': dayevents})

@method_decorator(login_required, name='dispatch')
class ScheduleCreate(CreateView): 
    model = Schedule 
    form_class = ScheduleForm
    template_name="schedule_create.html"
    def form_valid(self, form):
        self.object = form.save(commit = False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect('/user/'+str(self.object.user.id))

@method_decorator(login_required, name='dispatch')
class ScheduleDelete(DeleteView): 
    model = Schedule
    template_name = "schedule_delete_confirm.html"
    def get_success_url(self):
        return reverse('profile', kwargs={'id': self.object.user.id}) 

@method_decorator(login_required, name='dispatch')
class ScheduleUpdate(UpdateView): 
    model = Schedule 
    form_class = ScheduleUpdateForm
    template_name="schedule_update.html"
    def form_valid(self, form):
        self.object = form.save(commit = False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect('/schedule/'+str(self.object.id))

### DAYEVENTS 
@login_required
def DayEventCreate(request, id):
    schedule = get_object_or_404(Schedule, id=id)
    schedule_instance = schedule
    max_days = schedule.numdays
    schedulefilter = Schedule.objects.filter(id = id)
    eventfilter = Event.objects.filter(city=schedule.city)
    if request.method == 'POST': 
        form = DayEventForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/schedule/'+str(id))
    else: 
        form = DayEventForm(initial={'schedule':id})
        form.fields['schedule'].queryset = schedulefilter
        form.fields['event'].queryset = eventfilter
    return render(request, 'day_event_create.html', {'form': form, 'schedule': schedule})

@method_decorator(login_required, name='dispatch')
class DayEventDelete(DeleteView): 
    model = DayEvent
    template_name = "dayevent_delete_confirm.html"
    def get_success_url(self):
        return reverse('schedule_detail', kwargs={'id':self.object.schedule_id}) 

