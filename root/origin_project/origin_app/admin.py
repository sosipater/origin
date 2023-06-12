from django.contrib import admin
from .models import Chatbot, Message, Tag

@admin.register(Chatbot)
class ChatbotAdmin(admin.ModelAdmin):
    raw_id_fields = ('tags',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    raw_id_fields = ('tags',)

admin.site.register(Tag)