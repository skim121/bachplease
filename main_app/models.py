from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
# Create your models here.


User = get_user_model()

### City Model
CITY_CHOICES = (
    ("Austin", "Austin"),
    ("Nashville", "Nashville"),
    ("Miami", "Miami")
)

class City(models.Model): 
    name = models.CharField(max_length=250, choices = CITY_CHOICES )
    def __str__(self): 
        return self.name

### Tag Model 
class Tag(models.Model):
    name = models.CharField(max_length=250)
    def __str__(self): 
        return self.name
    

### Event Model 
BUDGET_CHOICES = (
    ("Free", "Free"),
    ("$", "$"),
    ("$$", "$$"),
    ("$$$", "$$$"),
    ("$$$$", "$$$$")
)

class Event(models.Model):
    name = models.CharField(max_length=250)
    budget = models.CharField(max_length=100, choices = BUDGET_CHOICES)
    description = RichTextField(blank=True, null=True)
    capacity = models.CharField(max_length = 250, blank=True, null = True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    neighborhood = models.CharField(max_length = 250, blank=True, null = True)
    image = models.ImageField(null = True, blank = True, upload_to="images/")
    website = models.CharField(max_length = 250, blank=True, null = True)
    tag = models.ManyToManyField(Tag, default=None, blank=True, related_name="event") 
    user = models.ManyToManyField(User, default=None, blank=True)
    def __str__(self): 
        return self.name


### Schedule Model 
class Schedule(models.Model):
    name = models.CharField(max_length=250)
    date_in = models.DateField()
    date_out = models.DateField()
    numdays = models.PositiveIntegerField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self): 
        return self.name

### DayEvent Model 
class DayEvent(models.Model): 
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    day = models.PositiveIntegerField()
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
