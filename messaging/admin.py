from django.contrib import admin
from .models import Conversation
from .models import ConversationMessage

admin.site.register(Conversation)
admin.site.register(ConversationMessage)
