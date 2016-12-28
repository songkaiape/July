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

urlpatterns = [
    url(r'^$', blog.IndexView.as_view()),
    url(r'^archive/(?P<cid>\d+)/$', blog.ArticleView.as_view()),
    url(r'^upload/$', csrf_exempt(blog.Upload.as_view())),
    url(r'^about/$', blog.AboutView.as_view()),
    url(r'^404/$', blog.NotFoundVIew.as_view()),
    url(r'^category/(?P<category_name>.+)/$', blog.CategoryListVIew.as_view()),
    url(r'^admin/', admin.site.urls),
]
