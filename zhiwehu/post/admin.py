# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin

from tinymce.widgets import TinyMCE

from .models import Category, Post, Comment


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 150, 'rows': 40}))

    class Meta:
        model = Post
        exclude = ('created', 'modified')


class PostAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'author', 'summary', 'view_count', 'like_count', 'created', 'modified'
    ]
    search_fields = [
        'title', 'content'
    ]
    form = PostForm


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'created']


def approve_comment(modeladmin, request, queryset):
    queryset.update(approved=True)

def disapprove_comment(modeladmin, request, queryset):
    queryset.update(approved=False)


approve_comment.short_description = 'Approve selected comments'


class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'post', 'content', 'parent', 'user', 'user_name', 'user_email', 'user_website', 'approved', 'created'
    ]
    search_fields = [
        'content'
    ]
    actions = [approve_comment]


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
