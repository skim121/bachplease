from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Home, name="home"),
    path('logout/', views.logout_view, name='logout'),
    path('austin/', views.AustinList.as_view(), name="austin_list"), 
    path('nashville/', views.NashvilleList.as_view(), name="nashville_list"), 
    path('miami/', views.MiamiList.as_view(), name="miami_list"), 
    path('event/<int:id>/', views.EventDetail, name="event_detail"),
    path('user/<int:id>/', views.profile, name="profile"),
    path('fav/<int:id>/', views.fav_add, name="fav_add"),
    path('schedule/<int:id>/', views.ScheduleDetail, name="schedule_detail"),
    path('schedule/create/', views.ScheduleCreate.as_view(), name="schedule_create"),
    path('schedule/<int:pk>/delete/', views.ScheduleDelete.as_view(), name="schedule_delete"),
    path('dayevent/create/', views.DayEventCreate.as_view(), name="day_event_create"),
    path('search/', views.FilterView, name="filter_view")
]
