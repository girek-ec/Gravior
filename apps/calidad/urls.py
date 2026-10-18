from django.urls import path

from . import views

app_name = 'calidad'

urlpatterns = [
    path('calidad-bioseguridad/', views.QualityView.as_view(), name='index'),
]
