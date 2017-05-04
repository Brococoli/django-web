from django.shortcuts import render,get_object_or_404

# Create your views here.

from django.http import HttpResponse
from .models import Post,Category
import markdown,pygments
from comments.forms import CommentForm
from django.db.models.aggregates import Count

def index(request):
	#render 会生成一个HttpResponse
	#request是预览器的请求
	#'blog/index.html'是模板的位置，在settings中配置过了，就是根目录/blog/index.html
	#context是文本内容，模板中要替换的
	# return render(request, 'blog/index.html', context={
	# 		'title':'我的博客首页',
	# 		'welcome':'欢迎访问我的博客首页'
	# 	})

	post_list = Post.objects.all().order_by('-created_time')
	# .order_by('-created_time') 表示按'created_time' 排序，'-' 表示按逆序
	return render(request, 'blog/index.html', context={
			'post_list':post_list
		})

def detail(request, pk):
	# get_object_or_404表明getPost中pk的信息，不存在就raise一个404错误
	post = get_object_or_404(Post, pk=pk)
	post.body = markdown.markdown(post.body,extensions=[
									  'markdown.extensions.extra', #extra扩展
									  'markdown.extensions.codehilite', #代码高亮
									  'markdown.extensions.toc' #目录支持
								  ])
	# 获取该post下的全部评论
	form = CommentForm()
	# 获取这篇 post 下的全部评论
	comment_list = post.comment_set.all()
	context = {
		'post': post,
		'form': form,
		'comment_list': comment_list
	}


	return render(request, 'blog/detail.html', context = context)


def archives(request, year, month):
	post_list = Post.objects.filter(created_time__year=year, created_time__month=month)
	return render(request, 'blog/index.html', context={
			'post_list' : post_list
		})

def category(request, pk):
	cate = get_object_or_404(Category, pk=pk)
	post_list = Post.objects.filter(category=cate)
	# post_list = Post.objects.filter(category__pk=pk) 也可以

	# annotate计算该分类下post(文章)数量，保存在num_posts，直接可以category.num_posts使用
	# 并且所有文章也会保存在category_list中
	category_list = Category.objects.annotate(num_posts = Count('post'))
	return render(request, 'blog/index.html', context={
			'post_list' : post_list,
		})

def fullscreen(request):
	post_list = Post.objects.all()

	return render(request, 'blog/fullscreen.html', context={ 'post_list':post_list })

def search(request):
	q = request.GET.get('q') # 得到搜索的文本
	error_msg = ''

	if not q: # 无输入
		error_msg = '请输入关键词'
		return render(request, 'blog/index,html', { 'error_msg':error_msg })

	post_list = Post.objects.filter(title__icontains=q) # title.icontain=q 标题包含q的文章
	return render(request, 'blog/index.html', {
			'error_msg':error_msg,
			'post_list':post_list,
		})