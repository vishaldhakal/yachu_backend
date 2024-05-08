from django.contrib import admin
from django.db import models
from .models import Author,Category,Post,Tag,Event
from unfold.admin import ModelAdmin
from tinymce.widgets import TinyMCE

admin.site.register(Author,ModelAdmin)
admin.site.register(Category,ModelAdmin)
admin.site.register(Tag,ModelAdmin)
admin.site.register(Event,ModelAdmin)

class PostAdmin(ModelAdmin):
   formfield_overrides = {
      models.TextField: {
            "widget": TinyMCE,
      },
   }

admin.site.register(Post,PostAdmin)