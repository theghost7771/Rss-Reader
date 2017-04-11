# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.cache import cache
import uuid


@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    telegram_chat_id = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    def get_telegram_auth_url(self):
        if self.telegram_chat_id:
            return
        # generate or get telegram authorization ID
        cache_key = 'telegram_auth:{}'.format(self.id)
        telegram_auth_id = cache.get(cache_key)
        if not telegram_auth_id:
            telegram_auth_id = uuid.uuid4().hex
            cache.set(cache_key, telegram_auth_id)
            cache.set('telegram_auth_id:{}'.format(telegram_auth_id), self.id)

        return 'https://telegram.me/{}?startasd={}'.format(settings.TELEGRAM_BOT_NAME, telegram_auth_id)
