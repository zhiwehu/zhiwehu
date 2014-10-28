# -*- coding: utf-8 -*-
# Import the basic Django ORM models library
from django.db import models

from model_utils.models import TimeStampedModel
from taggit.managers import TaggableManager
from autoslug.fields import AutoSlugField

from users.models import User


class Category(TimeStampedModel):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='title', unique=True)
    description = models.TextField(max_length=1024, blank=True, null=True)
    thumbnail_url = models.URLField(blank=True, null=True)

    def __unicode__(self):
        return self.title

    @property
    def post_count(self):
        return self.post_set.count()


# Post model
class Post(TimeStampedModel):
    category = models.ForeignKey(Category)
    author = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='title', unique=True)
    content = models.TextField()
    summary = models.CharField(max_length=1024, blank=True, null=True)
    tags = TaggableManager(blank=True)
    thumbnail_url = models.URLField(blank=True, null=True)
    view_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return self.title

    @property
    def comment_count(self):
        return self.comment_set.filter(approved=True).count()

    def approved_comments(self):
        return self.comment_set.filter(approved=True, parent__isnull=True)


class Comment(TimeStampedModel):
    post = models.ForeignKey(Post)
    content = models.CharField(max_length=1024)
    user = models.ForeignKey(User, blank=True, null=True)
    user_name = models.CharField(max_length=255, blank=True, null=True)
    user_email = models.EmailField(max_length=255, blank=True, null=True)
    user_website = models.URLField(max_length=255, blank=True, null=True)
    parent = models.ForeignKey('self', blank=True, null=True)
    approved = models.BooleanField(default=False)

    def __unicode__(self):
        return self.content

    def approved_replies(self):
        return self.comment_set.filter(approved=True)

    @property
    def json(self):
        user_id = None
        if self.user:
            user_id = self.user.id

        parent_id = None
        if self.parent:
            parent_id = self.parent.id

        return {
            'post_id': self.post.id,
            'content': self.content,
            'user_id': user_id,
            'parent_id': parent_id,
            'user_name': self.user_name,
            'user_email': self.user_email,
            'user_website': self.user_website,
        }
