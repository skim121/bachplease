from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('logout/', views.logout_view, name='logout'),
    path('austin/', views.AustinList.as_view(), name="austin_list"), 
    path('event/<int:id>/', views.EventDetail, name="event_detail"),
    path('user/<int:id>/', views.profile, name="profile"),
    path('fav/<int:id>/', views.fav_add, name="fav_add"),
    path('schedule/<int:id>/', views.ScheduleDetail, name="schedule_detail"),

]
