from django.contrib import admin

from .models import categories, Sentence

admin.site.register(categories)
admin.site.register(Sentence)
