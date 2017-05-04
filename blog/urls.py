from django.conf.urls import url 

from . import views

# app_name 表示这个urls.py文件是属于blog的
app_name = 'blog'
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^post/(?P<pk>\d+)/$', views.detail, name='detail'),
	#匹配到<网站域名>/post/2/就从views.detail类中生成html文件
	#(?P<pk>[0-9]+) 表示命名捕获组，其作用是从用户访问的 url 里把括号内匹配的字符串捕获并作为关键字参数传给视图函数 detail。
	#如url为/post/23/ 就匹配23 传给detail
	# 就是调用render(requeset, pk = 23)
	url(r'^archives/(?P<year>\d{4})/(?P<month>\d{1,2})/$', views.archives, name='archives'),
	# /archives/2017/4/
	url(r'^category/(?P<pk>\d+)/$', views.category, name='category'),
	url(r'^fullscreen/$', views.fullscreen, name='fullscreen'),
	url(r'^search/$', views.search, name = 'search'),
]