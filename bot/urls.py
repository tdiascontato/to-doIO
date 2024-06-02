from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('send_message/', views.send_message, name='send_message'),
    path('add_user/', views.add_user, name='add_user'),
    path('twilio_webhook/', views.twilio_webhook, name='twilio_webhook'),
]
