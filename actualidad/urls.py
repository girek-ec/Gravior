from django.urls import path

from . import views

app_name = 'actualidad'

urlpatterns = [
    path('actualidad/', views.PostListView.as_view(), name='index'),
    # Maqueta del detalle; en el bloque E se resuelve por slug contra Post.
    path('actualidad/<slug:slug>/', views.PostDetailView.as_view(), name='detail'),
]
