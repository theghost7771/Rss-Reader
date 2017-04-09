from django.db import models
from rss_reader.users.models import User

# Create your models here.

class Feed(models.Model):
    name = models.CharField(max_length=300)
    is_active = models.BooleanField(_('active'), default=True)
    url = models.URLField()
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class FeedItem(models.Model):
    title = models.CharField(max_length=300)
    is_active = models.BooleanField(_('active'), default=True)
    description = models.CharField(max_length=2000)
    pub_date = models.DateTimeField()
    url = models.URLField()
    created = models.DateTimeField(auto_now=True)
