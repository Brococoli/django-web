from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Category(models.Model):
	""" django 要求我们必须继承 models.Model 类，
    Category 只需要一个简单的分类名 name 就可以了。

    CharField 指定了 name 的数据类型，
    CharField 是字符型，
    max_length 指定其最大长度，
    超过这个长度的分类名就不能被存入数据库。

    当然 django 还为我们提供了各种各样的类型，
    如日期时间类型 DateTimeField、
    整数类型 IntegerField 等等。
    django 内置的类型全部类型可查看文档：
    https://docs.djangoproject.com/en/1.10/ref/models/fields/#field-types
    """

    #类名
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class Tag(models.Model):
	"""标签Tag"""

	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class Post(models.Model):
	"""文章的数据表"""
	
	#文章标题
	title = models.CharField(max_length=70)

	body = models.TextField()

	#创建时间，修改时间
	created_time = models.DateTimeField()
	modified_time = models.DateTimeField()

	#文章摘要
	excerpt = models.CharField(max_length=200, blank=True)

	#文章分类
	category = models.ForeignKey(Category)
	tags = models.ManyToManyField(Tag, blank=True)

	#文章作者
	author = models.ForeignKey(User)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('blog:detail', kwargs={'pk':self.pk})
	# blog:detaill 指的是 app_name 为blog下的 detail函数
	# 我们在blog/urls.py
	# 通过 app_name = 'blog' 告诉了 django 这个 URL 模块是属于 blog 应用的，因此 django 能够顺利地找到 blog 应用下 name 为 detail 的视图函数
	# reverse会根据urls.py中 blog app下名字为detail匹配方法中正则表达式r'^post/(?P<pk>[0-9]+)/$' 中pk参数用self.pw替换，reverse返回的是一个链接'/post/23/'

	class Meta:
		ordering = ['-created_time','title']