# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r"list/$",
        view=views.FeedListView.as_view(),
        name="list"
    ),
    url(
        regex=r"(?P<pk>\d+)/update/$",
        view=views.FeedUpdateView.as_view(),
        name="update"
    ),
    url(
        regex=r"add/$",
        view=views.FeedCreateView.as_view(),
        name="create"
    )
]
