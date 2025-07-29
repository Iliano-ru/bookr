from django.urls import path
from . import views

urlpatterns = [
    path('publishers/<int:pk>/', views.publisher_edit, name='publisher_edit'),
    path('publishers/new/', views.publisher_edit)
]