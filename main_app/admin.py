from django.contrib import admin
from .models import Event, Schedule, City, Tag, DayEvent
# Register your models here.

admin.site.register(Event)
admin.site.register(Schedule)
admin.site.register(City)
admin.site.register(Tag)
admin.site.register(DayEvent)
