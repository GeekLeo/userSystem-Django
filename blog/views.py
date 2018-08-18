from django.shortcuts import render, redirect
from . import forms
from . import models
from login.models import User


# Create your views here.

def index(request):
    blog_list = models.Blog.objects.order_by('-m_time').order_by('-c_time')
    return render(request, 'blog/index.html', locals())


def create(request):
    if not request.session.get('is_login', None):
        return redirect('home')
    if request.session['user_name'] != "testUser":
        return redirect('home')
    if request.method == "POST":
        create_blog_form = forms.CreateBlogForm(request.POST)
        message = "Please check the field"
        if create_blog_form.is_valid():
            blogname = create_blog_form.cleaned_data['name']
            summary = create_blog_form.cleaned_data['summary']
            content = create_blog_form.cleaned_data['content']
            same_name_blog = models.Blog.objects.filter(name=blogname)
            if same_name_blog:
                message = "该博客的主题已存在，请更换主题！"
                return render(request, 'blog/create.html', locals())
            new_blog = models.Blog(name=blogname, summary=summary, content=content)
            new_blog.save()
            message = "博客已成功发布！"
        return render(request, 'blog/create.html', locals())
    create_blog_form = forms.CreateBlogForm()
    return render(request, 'blog/create.html', locals())


def edit(request):
    pass


def detail(request, blog_id):
    blog = models.Blog.objects.get(pk=blog_id)
    comments = models.Comment.objects.filter(blog_id=blog_id)
    return render(request, 'blog/detail.html', locals())


def comment(request):
    if request.method == "POST":
        # comment_form = forms.CommentForm(request.POST)

        # message = "Please check the field"
        # if comment_form.is_valid():
        #     text = comment_form.cleaned_data['text']
        text = request.POST.get('text')
        blog_id = request.POST.get('blog_id')
        user_id = request.POST.get('user_id')
        try:
            blog = models.Blog.objects.get(pk=blog_id)
            try:
                user = User.objects.get(pk=user_id)
            except:
                message = "无权限评论"
                return render(request, 'blog/detail.html', locals())
        except:
            message = "不存在该博客"
            return render(request, 'blog/detail.html', locals())
        if not text or not text.strip():
            message = "请输入评论内容"
            return render(request, 'blog/detail.html', locals())
            # return redirect('blog:detail', blog_id=blog_id, message=message)
        new_comment = models.Comment(text=text, blog_id=blog_id, user_id=user_id)
        new_comment.save()
        return redirect('blog:detail', blog_id=blog_id)
    # return render(request, 'blog/detail.html', locals())
# comment_form = forms.CommentForm()
# return render(request, 'blog/detail.html', locals())
