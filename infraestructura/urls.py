from django.urls import path

from core.views import PendingDetailView

from . import views

app_name = 'infraestructura'

urlpatterns = [
    path('instalaciones/', views.FacilityListView.as_view(), name='index'),
    # Detalle por slug: se implementa en el bloque C.
    path('instalaciones/<slug:slug>/', PendingDetailView.as_view(), name='detail'),
]
