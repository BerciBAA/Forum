from django.contrib import admin
from .models import ForumRoom, Message, Topic

admin.site.register(Topic)
admin.site.register(ForumRoom)
admin.site.register(Message)
