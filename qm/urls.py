from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "history/",
        views.history,
        name="history"
    ),

    path(
        "history/<int:pk>/",
        views.history_detail,
        name="history_detail"
    ),

    path(
        "delete/<int:pk>/",
        views.delete_history,
        name="delete_history"
    ),

    path(
        "clear-history/",
        views.clear_history,
        name="clear_history"
    ),

]