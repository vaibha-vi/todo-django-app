from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('complete/<int:id>/', views.complete_task, name='complete'),
    path('delete/<int:id>/', views.delete_task, name='delete'),
]