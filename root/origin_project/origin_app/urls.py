from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('send_message/', views.chat, name='send_message'),
    path('chat_interface/', views.chat_interface, name='chat_interface'),
    path('chat/', views.chat, name='chat'),
    path('fetch_history/', views.fetch_history, name='fetch_history'),
    path('chatbots/', views.chatbot_list, name='chatbot_list'),
]
