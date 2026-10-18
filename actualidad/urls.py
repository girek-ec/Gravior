from django.urls import path

from core.views import PendingDetailView

from . import views

app_name = 'actualidad'

urlpatterns = [
    path('actualidad/', views.PostListView.as_view(), name='index'),
    # Detalle por slug: se implementa en el bloque E.
    path('actualidad/<slug:slug>/', PendingDetailView.as_view(), name='detail'),
]
