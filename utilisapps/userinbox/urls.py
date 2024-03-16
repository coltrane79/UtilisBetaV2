from django.urls import path

from . import views

urlpatterns = [
    path("inbox/", views.inbox, name="user_inbox"),
]
