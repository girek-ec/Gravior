from django.urls import path

from . import views

app_name = 'aliados'

urlpatterns = [
    path('aliados/', views.PartnerView.as_view(), name='index'),
]
