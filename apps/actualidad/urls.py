from django.urls import path

from . import views

app_name = 'actualidad'

urlpatterns = [
    path('actualidad/', views.PostListView.as_view(), name='index'),
    path('actualidad/<slug:slug>/', views.PostDetailView.as_view(), name='detail'),
]
