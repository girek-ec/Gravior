from django.urls import path

from core.views import PendingDetailView

from . import views

app_name = 'genetica'

urlpatterns = [
    path('genetica/', views.GeneticLineListView.as_view(), name='index'),
    # Detalle por slug: se implementa en el bloque B.
    path('genetica/<slug:slug>/', PendingDetailView.as_view(), name='detail'),
]
