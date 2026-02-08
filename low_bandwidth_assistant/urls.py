from django.urls import path
from assistant import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/query/', views.api_query, name='api_query'),
]
