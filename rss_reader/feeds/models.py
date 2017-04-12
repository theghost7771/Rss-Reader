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
    filters = ArrayField(models.CharField(max_length=50), size=10, default=list, blank=True,
                         help_text=_('Comma separated.'
                                     'Add items only if one of this words present in feed title or description'))
    rss_title = models.CharField(max_length=500, default='')
    rss_modified = models.DateTimeField(null=True)
    rss_etag = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    url = models.URLField()
    user = models.ForeignKey(User)
    telegram_notifications = models.BooleanField(default=False,
                                                 help_text=_('Send notifications about new feed items to telegram'))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created']

    def collect_items(self):
        """Collect and return all new items in feed.
        Modifying current feed.rss_modified/etag/title, and saves it to db.
        Also generate 1 request to get last feed items. (2 requests in sum, be careful)
        return list of new feed items to create in DB"""
        kwargs = {}
        if self.rss_etag:
            kwargs['etag'] = self.rss_etag
        if self.rss_modified:
            kwargs['modified'] = self.rss_modified

        data = feedparser.parse(self.url, **kwargs)

        # TODO: refactor. Maybe we don't need this dances with modified/published. RTFM feedparser.
        # use OR here to prevent traceback if modified_parsed present, and published parsed not
        modified_date = data.get('modified_parsed') or data.feed.published_parsed
        rss_modified = datetime.fromtimestamp(mktime(modified_date)).replace(tzinfo=timezone.utc)
        if self.rss_modified == rss_modified:
            return []
        self.rss_modified = rss_modified
        self.rss_etag = data.get('rss_etag', '')
        self.rss_title = data.feed.title

        to_create = []
        # Retrieve last feed items, for additional protection from duplicates
        last_feeds = FeedItem.objects.values_list('url', flat=True).filter(feed=self)[:len(data.entries) * 2]

        for item in data.entries:
            # continue if we already have feed item with such url
            if item.link in last_feeds:
                continue
            # if filters specified, at least 1 filter have to match
            if self.filters and not any(f.lower() in (item.title + item.summary).lower() for f in self.filters):
                continue

            to_create.append(FeedItem(
                title=item.title,
                url=item.link,
                description=item.summary[:2000],
                pub_date=datetime.fromtimestamp(mktime(item.published_parsed)).replace(tzinfo=timezone.utc),
                feed=self,
            ))

        return to_create


class FeedItem(models.Model):
    title = models.CharField(max_length=300)
    is_active = models.BooleanField(_('active'), default=True)
    description = models.CharField(max_length=2000)
    pub_date = models.DateTimeField()
    url = models.URLField()
    created = models.DateTimeField(auto_now=True)
    feed = models.ForeignKey(Feed)

    class Meta:
        ordering = ['-pub_date']

# Just to remember. Maybe we need to normalize Feed.filter, maybe not?
# class Filter(models.Model):
# """Filer for Feed"""
#     condition =
#     value =
#     feed = models.ForeignKey(Feed)
