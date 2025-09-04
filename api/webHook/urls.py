from django.urls import path
from . import views

urlpatterns = [
    path('webhook-receiver/', views.receive_webhook, name='webhook_receiver'),
    path('trigger-webhook/', views.trigger_local_webhook, name='trigger_webhook'),
]