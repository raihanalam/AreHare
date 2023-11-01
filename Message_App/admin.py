from django.contrib import admin

from .models import ChatRoom, Chat as ChatMessage

# Register your models here.
admin.site.register(ChatRoom)
admin.site.register(ChatMessage)