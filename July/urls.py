"""July URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from blog import views as blog
from django.views.decorators.csrf import csrf_exempt
from blog.feeds import RssSiteNewsFeed, AtomSiteNewsFeed

from django.contrib.sitemaps.views import sitemap
from blog.sitemap import BlogSitemap

sitemaps = {
    'static': BlogSitemap,
}
urlpatterns = [
    url(r'^$', blog.IndexView.as_view(), name="index"),
    url(r'^article/(?P<article_url>.*)/$', blog.ArticleView.as_view(), name='article'),
    url(r'^upload/$', csrf_exempt(blog.Upload.as_view())),
    url(r'^about/$', blog.AboutView.as_view(), name='about'),
    url(r'^category/(?P<category_name>.+)/$', blog.CategoryListVIew.as_view(), name='category'),
    url(r'^admin/', admin.site.urls),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^rss\.xml$', RssSiteNewsFeed()),
    url(r'^atom\.xml$', AtomSiteNewsFeed()),
]
