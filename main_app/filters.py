import django_filters
from django import forms 
from django.contrib.auth.models import User 
from .models import *


class EventFilter(django_filters.FilterSet): 
    tag = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta: 
        model = Event
        fields = ['city', 'tag']
     