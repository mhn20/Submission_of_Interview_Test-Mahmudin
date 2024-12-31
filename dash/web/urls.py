from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("list-movies/", views.listMovie, name="index_listMovie"),
    path("detail-movie/<int:idxrow>/",
         views.detailMovie, name="index_detailMovie"),
]
