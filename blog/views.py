from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import FormView, ListView, DateDetailView
from django.core.paginator import Paginator
from blog import models

from django.conf import settings
from datetime import datetime
import time
import json
import os


# Create your views here.

class MeInfo(object):
    def get_webhead(self):
        return models.Settings.objects.filter(id=1).values('title', 'keywords', 'description')[0]

    def get_category_list(self):
        # 获取分类列表
        category_list = list(models.Categories.objects.all().values('id', 'name'))
        # 添加分类次数
        for category in category_list:
            count = models.Article.objects.filter(categories__id=category['id']).count()
            category['count'] = count
        return category_list

    def get_links(self):
        # 友情链接
        return models.Links.objects.all().values('name', 'url')

    def get_icons(self):
        return list(models.AboutIcon.objects.all().values('icon', 'url'))

    def get_about(self):
        return models.About.objects.all().values('name', 'avatar', 'declaration')[0]


class IndexView(ListView, MeInfo):
    def get(self, request, *args, **kwargs):

        try:
            page = int(request.GET.get('page', 1))  # 页码
        except Exception as e:
            return HttpResponseRedirect('/404')

        # 站点Title信息
        webhead = self.get_webhead()
        # 分类信息
        category_list = self.get_category_list()

        # 文章列表
        archives = models.Article.objects.filter(status='0').values('id', 'title', 'abstract', 'created_time',
                                                                    'categories__name')

        limit = 10  # 没页显示多少条
        paginator = Paginator(archives, limit)  # 实例化一个分页对象

        try:
            archives = paginator.page(page)  # 获取某页对应的记录
        except Exception as e:
            return HttpResponseRedirect('/404')

        # 加入标签
        for archive in archives:
            tags = list(models.Article.objects.filter(title=archive['title']).values('tag__name'))
            tag = ''
            for t in tags:
                tag += "#" + t['tag__name'] + " "
            tag.strip()
            archive['tag'] = tag

        # 友情链接
        links = self.get_links()
        # 图标
        icons = self.get_icons()
        # 关于我信息
        about = self.get_about()
        return render(request, 'index.html', locals())


class ArticleView(DateDetailView, MeInfo):
    def get(self, request, cid, *args, **kwargs):
        article = models.Article.objects.filter(id=cid).values('id', 'title', 'body', 'created_time',
                                                               'categories__name', 'created_time', 'last_modified_time')
        if len(article) == 1:
            article = article[0]
        else:
            return HttpResponseRedirect('/404')

        tags = list(models.Article.objects.filter(title=article['title']).values('tag__name'))
        tag = ''
        for t in tags:
            tag += "#" + t['tag__name'] + " "
        tag.strip()
        article['tag'] = tag
        webhead = {
            'title': article['title'],
            'keywords': article['tag'].replace('#', '').replace(' ', ',').strip(','),
            'description': article['body'][:200]
        }
        url = 'https://' + request.get_host() + request.get_full_path()  # 主机
        return render(request, 'archive.html', locals())


class Upload(FormView):
    def post(self, request, *args, **kwargs):
        result = {'success': 0, 'message': '长传错误！'}
        self.files = request.FILES.get('editormd-image-file', None)  # 获取文件对象
        if self.files:
            self.host = request.META['HTTP_ORIGIN']  # 上传者主题，用于返回URL
            self.file_name = request.GET.get('guid', str(time.time()).split('.')[0])  # 保存的文件名
            result = self.create_file()  # 创建文件
        return HttpResponse(json.dumps(result))

    def create_file(self):
        allow_file_type = ["jpg", "jpeg", "gif", "png"]  # 允许上传的文件类型
        file_type = self.files.name.split('.')[-1]  # 文件后缀
        if file_type not in allow_file_type:  # 上传的文件类型不匹配
            return {'success': 0, 'message': '文件格式不正确！'}
        dir_name = settings.MEDIA_ROOT + '/%d/%d/' % (datetime.today().year, datetime.today().month)  # 文件上传的路径
        if not os.path.exists(dir_name): os.makedirs(dir_name)  # 创建文件目录
        file_path = os.path.join(dir_name, str(self.file_name + '.' + file_type))  # 生成文件路径
        file_url = self.host + settings.MEDIA_URL + file_path.split(settings.MEDIA_URL)[-1]  # 文件的URL
        open(file_path, 'wb').write(self.files.file.read())  # 写入文件
        return {'success': 1, 'message': 'OK', 'url': file_url}


class CategoryListVIew(ListView, MeInfo):
    def get(self, request, category_name, *args, **kwargs):
        webhead = models.Categories.objects.filter(name=category_name).values('title', 'keywords', 'description')[0]
        archive_list = list(
            models.Article.objects.filter(categories__name=category_name).values('id', 'title', 'created_time'))
        if len(archive_list) == 0:
            return HttpResponseRedirect('/404')
        # 获取分类列表
        category_list = list(models.Categories.objects.all().values('id', 'name'))
        # 添加分类次数
        for category in category_list:
            count = models.Article.objects.filter(categories__id=category['id']).count()
            category['count'] = count
        # 友情链接
        links = self.get_links()
        # 图标
        icons = self.get_icons()
        # 关于我信息
        about = self.get_about()

        return render(request, 'category.html', locals())


class AboutView(DateDetailView, MeInfo):
    def get(self, request, *args, **kwargs):
        articleid = models.About.objects.all().values('article')[0]
        article = models.Article.objects.filter(id=articleid['article']).values('title', 'body')[0]
        tags = list(models.Article.objects.filter(title=article['title']).values('tag__name'))
        tag = ''
        for t in tags:
            tag += "#" + t['tag__name'] + " "
        tag.strip()
        article['tag'] = tag
        about = self.get_about()
        webhead = {
            'title': '关于 | ' + about['name'],
            'description': about['declaration'],
            'keywords': article['tag'].replace('#', '').replace(' ', ',').strip(',')
        }
        return render(request, 'about.html', locals())


class NotFoundVIew(DateDetailView, MeInfo):
    def get(self, request, *args, **kwargs):
        webhead = self.get_webhead()
        return render(request, '404.html', locals())
