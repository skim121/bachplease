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
from .forms import DayEventForm 
# from django.db.models import Q
# import django_filters 

def Home(request): 
    tags = Tag.objects.all()
    events = Event.objects.all()
    event_filter = EventFilter(request.GET, queryset = events)
    events = event_filter.qs
    return render(request, 'home.html', {'event_filter': event_filter, 'events':events})


def FilterView(request): 
    header = request.GET['city']
    tagresults = request.GET.getlist('tag')
    cityname = City.objects.filter(id=header).values_list('name', flat=True)
    tagname = Tag.objects.filter(id__in=tagresults)
    events = Event.objects.filter(tag__in=tagname, city=header)
    city_filter = CityFilter(request.GET, queryset = events)
    events = city_filter.qs
    return render(request, 'citylist.html', {'header': cityname, 'tags': tagname, 'events':events, 'city_filter': city_filter})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def AustinList(request): 
    events = Event.objects.filter(city=1)
    header = ["Austin"]
    city_filter = CityFilter(request.GET, queryset = events)
    events = city_filter.qs
    # events = event_filter.qs
    # header = request.GET.get('city__name')
    return render(request, 'citylist.html', {'city_filter': city_filter, "events": events, "header": header})


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
    # range = schedule.numdays
    looptimes = range(1, schedule.numdays+1)
    events = Event.objects.filter(user=request.user, city=schedule.city)
    dayevents = DayEvent.objects.filter(schedule=schedule.id)
    print(dayevents)
    return render(request, 'schedule_detail.html', {'schedule': schedule, 'events': events, 'looptimes': looptimes, 'dayevents': dayevents})

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

# class DayEventCreate(CreateView): 
#     model = DayEvent
#     form_class = DayEventForm
#     template_name = 'day_event_create.html'
#     # success_url ='/'
#     def get(self,request):
#         print(request.GET)
#         return HttpResponseRedirect('/')

def DayEventCreate(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    eventfilter = Event.objects.filter(city=schedule.city)
    if request.method == 'POST': 
        form = DayEventForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else: 
        form = DayEventForm(initial={'schedule':schedule_id})
        form.fields['event'].queryset = eventfilter
    return reverse(request, 'day_event_create.html', {'form': form})


