from django.urls import path
from . import views


app_name = 'bimamitra'
urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.home, name='home'),
    path('bimabot/', views.bimabot, name='bimabot'),
    path('about/', views.about, name='about'),
    path('contactus/', views.contactus, name='contactus'),
]