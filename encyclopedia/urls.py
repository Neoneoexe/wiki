from django.urls import path

from . import views

app_name = "paths"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.wiki, name="wiki"),
    path("search", views.search, name="search"),
    path("cnp/", views.cnp, name="cnp"),
    path("ran", views.random1, name="ran"),
    path("edit/<str:name>", views.edit, name="edit")
]
