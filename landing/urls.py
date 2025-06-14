from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('api/chat', views.api_chat, name='api_chat'),
    path('api/chat/health', views.api_chat_health, name='api_chat_health'),
]
