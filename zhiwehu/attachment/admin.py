from django.contrib import admin

from .models import ImageAttachment


admin.site.register(ImageAttachment, admin.ModelAdmin)
