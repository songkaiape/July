from django.db import models

# Create your models here.

__all__ = [
    'Categories',
    'Article',
    'Links',
    'Tag'
]


class Categories(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name='分类名称')
    title = models.CharField(max_length=64, verbose_name='标题')
    description = models.CharField(max_length=32, verbose_name='描述')
    keywords = models.CharField(max_length=255, verbose_name='关键词')

    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        verbose_name = '分类(Categories)'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return self.name


class Article(models.Model):
    STATUS_CHOICES = (
        ('0', '发布'),
        ('1', '草稿'),
    )

    title = models.CharField(max_length=32, unique=True, verbose_name='文章标题')
    url = models.CharField(max_length=255, verbose_name='链接', unique=True)
    abstract = models.TextField(verbose_name='摘要')
    body = models.TextField(verbose_name='文章内容')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)
    status = models.CharField(default='0', max_length=1, choices=STATUS_CHOICES, verbose_name='文章状态')
    categories = models.ForeignKey("Categories", verbose_name='分类')
    tag = models.ManyToManyField("Tag", verbose_name='标签')

    class Meta:
        verbose_name = '文章(Article)'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return self.title


class Links(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name='友情链接名字')
    url = models.URLField(unique=True, verbose_name='URL')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加日期')

    class Meta:
        verbose_name = '友情链接(Links)'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name='标签名称')
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        verbose_name = '标签(Tag)'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name
