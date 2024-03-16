from django.urls import path

from . import views

from .dash_apps import dash_elec_scorecard

urlpatterns = [
    path("regulator-open-data/", views.oeb_open_data, name="oeb_open_data"),
]
