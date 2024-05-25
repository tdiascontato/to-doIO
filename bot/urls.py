from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('webhook/', views.webhook, name='webhook'),
    path('send_message/', views.send_message, name='send_message'),
]
