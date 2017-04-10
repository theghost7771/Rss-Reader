# -*- coding: utf-8 -*-
from time import mktime
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
import feedparser

from rss_reader.users.models import User


class Feed(models.Model):
    name = models.CharField(max_length=300)
    filters = ArrayField(models.CharField(max_length=50), size=10, default=list,
                         help_text=_('Comma separated.'
                                     'Add items only if one of this words present in feed title or description'))
    rss_title = models.CharField(max_length=500, default='')
    rss_modified = models.DateTimeField(null=True)
    is_active = models.BooleanField(_('active'), default=True)
    url = models.URLField()
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def collect_items(self):
        data = feedparser.parse(self.url)

        rss_modified = datetime.fromtimestamp(mktime(data.modified_parsed)).replace(tzinfo=timezone.utc)
        if self.rss_modified == rss_modified:
            return []
        self.rss_modified = rss_modified
        self.rss_title = data.feed.title

        to_create = []
        for item in data.entries:

            if self.filters:
                # if filters exists, at least 1 must to match
                if not any(f.lower() in (item.title + item.summary).lower() for f in self.filters):
                    continue

            to_create.append(FeedItem(
                title=item.title,
                url=item.link,
                description=item.summary[:2000],
                pub_date=datetime.fromtimestamp(mktime(item.published_parsed)).replace(tzinfo=timezone.utc)
            ))

        self.save()
        return to_create


class FeedItem(models.Model):
    title = models.CharField(max_length=300)
    is_active = models.BooleanField(_('active'), default=True)
    description = models.CharField(max_length=2000)
    pub_date = models.DateTimeField()
    url = models.URLField()
    created = models.DateTimeField(auto_now=True)

# class Filter(models.Model):
# """Filer for Feed"""
#     condition =
#     value =
#     feed = models.ForeignKey(Feed)

