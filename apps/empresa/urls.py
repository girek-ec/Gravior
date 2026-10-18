from django.urls import path

from . import views

app_name = 'empresa'

urlpatterns = [
    path('nosotros/', views.AboutView.as_view(), name='index'),
]
