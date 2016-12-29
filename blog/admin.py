# _*_ coding:utf-8 _*_
from django.contrib import admin
from blog.models import *


# Register your models here.

class ArchiveAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'abstract', 'body', 'status', 'categories', 'tag',)
        }),

        ('更多设置', {
            'classes': ('collapse',),
            'fields': (),
        }),
    )
    list_display = ('id', 'title', 'categories', 'created_time', 'last_modified_time')

    class Media:
        css = {
            'all': ('/static/plugin/editor.md/editormd.css',)
        }
        js = (
            '/static/plugin/editor.md/jquery.min.js',
            '/static/plugin/editor.md/editormd.js',
            '/static/plugin/editor.md/config.js'
        )


admin.site.register(Article, ArchiveAdmin)


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'title', 'description', 'keywords', 'created_time', 'last_modified_time',)


admin.site.register(Categories, CategoriesAdmin)


class LinksAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url', 'add_time',)


admin.site.register(Links, LinksAdmin)


class SettingsAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'keywords',)


admin.site.register(Settings, SettingsAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_time', 'last_modified_time',)


admin.site.register(Tag, TagAdmin)


class AboutAdmin(admin.ModelAdmin):
    list_display = ('name', 'avatar', 'article', 'declaration',)


admin.site.register(About, AboutAdmin)


class AboutIconAdmin(admin.ModelAdmin):
    list_display = ('icon', 'url',)


admin.site.register(AboutIcon, AboutIconAdmin)
