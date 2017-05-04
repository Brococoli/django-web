from django.shortcuts import render,get_object_or_404, redirect
from blog.models import Post
from .models import Comment
from .forms import CommentForm

# Create your views here.

def post_comment(request, post_pk):
	# 根据文章的pk(数据库id) 获取post对象，若不存在就raise 404
	post = get_object_or_404(Post, pk = post_pk)

	# 检测是否是POST请求， POST时才能需要表单
	if request.method == 'POST':
		# 构造CommentForm实例, django会从POST提取信息按CommentForm 实例化表单
		form = CommentForm(request.POST)

		# form.is_vaild() django会帮我们自动检测表单数据是否合法, 合法返回True, 否则False
		if form.is_valid():
			# form.save(commit=False)表示 仅仅利用保单数据生成Comment模板类实例,但不保存到数据库
			comment = form.save(commit=False)

			#将评论和被评论的文章关联起来
			comment.post = post

			# 保存在数据库中
			comment.save()

			#从定向到post的详情页
			return redirect(post)
		else:
			# 检查数据不合法, 重新渲染详情页, 并且渲染表单的错误
			# 因此我们传了三个模板变量给 detail.html
            # 一个是文章(post), 一个是评论列表, 一个是表单 form

			# 因为Comment类中 含有post , 是多对一的关系 , comment->post ,查看这个评论属于哪个文章就是 comment.post
			# 查看这个文章有哪些评论 , 就是反向查询, post->comment, 就是 post.comment_set.all()
			comment_list = post.comment_set.all()
			context = {
				'post':post,
				'form':form,
				'comment_list':comment_list,
			}
			return render(request, 'blog/detail.html', context = context)

		# 不是post请求, 说明用户没有提交数据, 重定向到文章详情页
		return redirect(post)