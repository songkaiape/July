#!/use/bin/env python
# _*_ coding:utf-8 __

from django.contrib.syndication.views import Feed
from .models import Article
from django.utils.feedgenerator import Atom1Feed
from django.utils.feedgenerator import Rss201rev2Feed


class RssSiteNewsFeed(Feed):
    feed_type = Rss201rev2Feed
    author_name = "安生"
    title = "安生标题"
    link = "https://blog.ansheng.me/"
    description = "安生描述"

    def items(self):
        return Article.objects.all().order_by('-created_time')[:5]

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        return '/article/%s' % item.url


class AtomSiteNewsFeed(RssSiteNewsFeed):
    feed_type = Atom1Feed
    subtitle = RssSiteNewsFeed.description
