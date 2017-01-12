from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import FormView, View
from pure_pagination import Paginator
from .models import *
from django.conf import settings
from datetime import datetime
import time
import json
import os


# Create your views here.

class IndexView(View):
    def get(self, request):
        # 文章列表
        article_list = Article.objects.filter(status=0).values('id', 'title', 'url', 'abstract', 'created_time',
                                                               'categories__name')
        # 分页数据
        try:
            page = int(request.GET.get('page', 1))  # 页码
            page_size = Paginator(article_list, 10, request=request)  # 获取有多少页
            article_list = page_size.page(page)  # 获取指定页的数据
        except Exception as e:
            return HttpResponseRedirect('/')
        # 加入标签
        for article in article_list.object_list:
            tags = list(Article.objects.filter(title=article['title']).values('tag__name'))
            tag = ""
            for t in tags:
                tag += "#" + t['tag__name'] + " "
            tag.strip()
            article['tag'] = tag
        category_list = Categories.objects.all()
        # 添加分类次数
        for category in category_list:
            count = Article.objects.filter(categories__id=category.id).count()
            category.count = count
        # 友情链接
        links = Links.objects.all()
        return render(request, 'index.html', {
            'article_list': article_list,
            'category_list': category_list,
            'links': links,
        })


class ArticleView(View):
    def get(self, request, article_url):
        # 获取文章，可以是文章的ID和URL
        try:
            article_url = int(article_url)
            article = Article.objects.filter(id=article_url, status=0).first()
            return HttpResponseRedirect('/article/%s' % article.url)
        except ValueError as e:
            article = Article.objects.filter(url=article_url, status=0).first()
        # 是否获取到文章
        if not article:
            return HttpResponseRedirect('/404')
        # 获取文章所有标签
        tags = list(Article.objects.filter(title=article.title).values('tag__name'))
        tag = ''
        for t in tags:
            tag += "#" + t['tag__name'] + " "
        tag.strip()
        title = article.title  # 标题
        keywords = tag.replace('#', '').replace(' ', ',').strip(',')  # 关键字
        description = article.body[:200]  # 描述
        url = 'https://' + request.get_host() + request.get_full_path()  # 主机
        return render(request, 'article.html', locals())


class Upload(FormView):
    def post(self, request, *args, **kwargs):
        result = {'success': 0, 'message': '长传错误！'}
        self.files = request.FILES.get('editormd-image-file', None)  # 获取文件对象
        if self.files:
            self.host = request.META['HTTP_ORIGIN']  # 上传者主题，用于返回URL
            self.file_name = str(time.time()).split('.')[0]  # 保存的文件名
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


class CategoryListVIew(View):
    def get(self, request, category_name):
        archive_list = list(
            Article.objects.filter(categories__name=category_name, status=0).values('url', 'title', 'created_time'))
        if len(archive_list) == 0:
            return HttpResponseRedirect('/404')

        category_list = Categories.objects.all()
        # 添加分类次数
        for category in category_list:
            count = Article.objects.filter(categories__id=category.id).count()
            category.count = count
        # 友情链接
        links = Links.objects.all()
        return render(request, 'category.html', locals())


class AboutView(View):
    def get(self, request):
        article = Article.objects.filter(id=1).first()
        return render(request, 'about.html', locals())
