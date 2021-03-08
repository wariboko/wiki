from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.get_title, name="title"),
    path("wiki/search/", views.search, name="search"),
    path("random/", views.random, name="random"),
    path("wiki/create/", views.create, name="add"),
    path("wiki/edit/", views.edit, name="edit"),
    path("wiki/save/", views.save, name="save")

    
]
