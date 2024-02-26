from django.contrib import admin

from .models import *

class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ("name", )}

admin.site.register(User)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)