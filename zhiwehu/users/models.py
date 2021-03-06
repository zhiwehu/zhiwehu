# -*- coding: utf-8 -*-
# Import the AbstractUser model
from django.contrib.auth.models import AbstractUser

# Import the basic Django ORM models library
from django.db import models

from django.utils.translation import ugettext_lazy as _


# Subclass AbstractUser
class User(AbstractUser):
    website = models.URLField(max_length=255, blank=True, null=True)
    avatar_url = models.URLField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.username