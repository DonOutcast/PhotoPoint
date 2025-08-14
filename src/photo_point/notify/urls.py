from django.urls import path
from .views import notify_view

urlpatterns = [
    path("", notify_view, name="notify"),
]
