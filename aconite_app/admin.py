from django.contrib import admin
from aconite_app.models import *


class LanguageInline(admin.TabularInline):
    model = Work.languages.through


class LocationInline(admin.TabularInline):
    model = Work.locations.through


class InspirationInline(admin.TabularInline):
    model = Work.inspirations.through


class WorkAdmin(admin.ModelAdmin):
    inlines = [LanguageInline, LocationInline, InspirationInline]
    fields = ['title', 'authors', 'original_title', 'dedication', 'year_demo', 'year', 'month', 'day', 'is_translation',
              'genre']


class ContentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Work, WorkAdmin)
admin.site.register(Content, ContentAdmin)

