# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import PostListView, PostDetailView

urlpatterns = patterns('',
                       # URL pattern for the PostListView  # noqa
                       url(
                           regex=r'^$',
                           view=PostListView.as_view(),
                           name='post_list'
                       ),

                       url(
                           regex=r'^category/(?P<category>[\w-]+)/$',
                           view=PostListView.as_view(),
                           name='category_post_list'
                       ),

                       url(
                           regex=r'^tag/(?P<tag>[\w-]+)/$',
                           view=PostListView.as_view(),
                           name='tag_post_list'
                       ),

                       url(
                           regex=r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$',
                           view=PostListView.as_view(),
                           name='archive_post_list'
                       ),

                       url(
                           regex=r'^blog/(?P<slug>[\w-]+)/$',
                           view=PostDetailView.as_view(),
                           name='post_detail'
                       ),

                       url(
                           regex=r'^add/comment/$',
                           view='post.views.add_comment',
                           name='add_comment',
                       ),
)