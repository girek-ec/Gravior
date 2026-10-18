from django.urls import path

from . import views

app_name = 'contacto'

urlpatterns = [
    path('contacto/', views.ContactView.as_view(), name='index'),
]
