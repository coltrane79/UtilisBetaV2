from django.urls import path

from . import views

urlpatterns = [
    path("inbox/", views.inbox, name="user_inbox"),
    path("inbox/change_password/", views.change_password, name="user_chg_pswd"),
]
