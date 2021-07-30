from django.urls import path
from .views import GetNotifications

urlpatterns = [
    path('get/', GetNotifications.as_view())
]