from datetime import timedelta
from django.db import models
from django.db.models import permalink
from django.core import signing
from django.utils.dateparse import parse_date
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from model_utils.fields import AutoCreatedField, AutoLastModifiedField
from model_utils.managers import QueryManager
from model_utils.models import StatusModel

ONE_DAY = timedelta(days=1)


class Article(StatusModel):
    STATUS = Choices(
        ('draft', _('draft')),
        ('published', _('published')),
    )

    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(_('slug'), max_length=100, help_text=_(
        'Unique identifier of the post, will be part of the URL.'
    ))
    excerpt = models.TextField(
        _('excerpt'), blank=True, max_length=400, help_text=_(
            'Short abstract of contents, will be displayed on list and '
            'main pages. Use Markdown syntax.'
        )
    )
    text = models.TextField(_('text'), help_text=_(
        'Use Markdown syntax.'
    ))
    created = AutoCreatedField(_('created at'), editable=True)
    modified = AutoLastModifiedField(_('last modified at'))

    objects = models.Manager()
    published = QueryManager(status=STATUS.published)

    signer = signing.TimestampSigner(salt="article")

    class Meta:
        ordering = ('-created',)

    @property
    def is_published(self):
        return self.status == self.STATUS.published

    def publish(self, commit=True):
        self.status = self.STATUS.published
        if commit:
            self.save()

    def signed_id(self):
        return self.signer.sign(str(self.pk))

    def is_signed_id(self, signature):
        try:
            pk = self.signer.unsign(signature, max_age=ONE_DAY.total_seconds())
            return str(self.pk) == pk
        except signing.BadSignature:
            return False

    @permalink
    def get_absolute_url(self):
        if self.status == self.STATUS.published:
            return 'article_detail', (), {'slug': self.slug}
        else:
            kwargs = {'slug': self.slug, 'signature': self.signed_id()}
            return 'article_preview', (), kwargs

