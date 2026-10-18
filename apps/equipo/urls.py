from django.urls import path

from . import views

app_name = 'equipo'

urlpatterns = [
    path('equipo/', views.TeamView.as_view(), name='index'),
]
