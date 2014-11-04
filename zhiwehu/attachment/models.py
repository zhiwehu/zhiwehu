from django.db import models
from model_utils.models import TimeStampedModel

from .utils import get_attachment_filename


class ImageAttachment(TimeStampedModel):
    file = models.ImageField(upload_to=get_attachment_filename)

    def __unicode__(self):
        return self.file.url
