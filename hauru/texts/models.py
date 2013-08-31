from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from model_utils.models import TimeStampedModel, StatusModel


class Article(TimeStampedModel, StatusModel):
    STATUS = Choices(
        ('draft', _('draft')),
        ('published', _('published'))
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100)
    text = models.TextField()

