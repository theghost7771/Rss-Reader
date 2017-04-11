# -*- coding: utf-8 -*-
from django.views.generic import ListView, UpdateView, CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import ugettext as _
from braces.views import LoginRequiredMixin

from .models import Feed, FeedItem
from .forms import FeedForm


class FeedActionMixin(object):
    model = Feed
    form_class = FeedForm
    success_url = reverse_lazy('feeds:list')

    @property
    def success_msg(self):
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        form.instance.user = self.request.user
        return super(FeedActionMixin, self).form_valid(form)


class FeedListView(LoginRequiredMixin, ListView):
    model = Feed
    context_object_name = 'feeds'
    template_name = 'feeds/list.html'

    def get_queryset(self):
        queryset = super(FeedListView, self).get_queryset()
        return queryset.filter(user=self.request.user)


class FeedCreateView(LoginRequiredMixin, FeedActionMixin, CreateView):
    model = Feed
    success_msg = _('Created')

    def get_queryset(self):
        queryset = super(FeedCreateView, self).get_queryset()
        return queryset.filter(user=self.request.user)


class FeedUpdateView(LoginRequiredMixin, FeedActionMixin, UpdateView):
    model = Feed
    success_msg = _('Updated')

    def get_queryset(self):
        queryset = super(FeedUpdateView, self).get_queryset()
        return queryset.filter(user=self.request.user)


class FeedItemListView(LoginRequiredMixin, ListView):
    model = FeedItem
    context_object_name = 'feed_items'
    template_name = 'feeds/item_list.html'

    def get_queryset(self):
        queryset = super(FeedItemListView, self).get_queryset()
        # to make sure we get only users feeds
        queryset = queryset.filter(feed__in=self.request.user.feed_set.all())
        # TODO: unit test for this, need try to get foreign feeds
        if 'feed' in self.request.GET:
            queryset = queryset.filter(feed_id=self.request.GET.get('feed'))

        return queryset
