from django.shortcuts import render, redirect
from . import forms
from . import models
from login.models import User


# Create your views here.

def index(request):
    blog_list = models.Blog.objects.filter(is_deleted=False).order_by('-m_time').order_by('-c_time')
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


def edit(request, blog_id):
    if not request.session.get('is_login', None):
        return redirect('home')
    if request.session['user_name'] != "testUser":
        return redirect('home')
    if request.method == "POST":
        blog_name = request.POST.get('blog_name')
        blog_summary = request.POST.get('summary')
        blog_content = request.POST.get('content')
        if not blog_name or not blog_summary or not blog_content or not blog_name.strip() or not blog_summary.strip() or not blog_content.strip():
            message = 'Please check the field'
            return render(request, 'blog/edit.html', locals())
        same_name_blog = models.Blog.objects.exclude(pk=blog_id).filter(name=blog_name)
        if same_name_blog:
            message = "该博客的主题已存在，请更换主题！"
            return render(request, 'blog/edit.html', locals())
        try:
            blog = models.Blog.objects.get(pk=blog_id)
            blog.name = blog_name
            blog.summary = blog_summary
            blog.content = blog_content
            blog.save()
            return redirect('blog:detail', blog_id=blog_id)
        except:
            message = '不存在该博客！'
        return render(request, 'login/index.html',locals())

    try:
        blog = models.Blog.objects.get(pk=blog_id)
        blog_name = blog.name
        blog_summary = blog.summary
        blog_content = blog.content
        return render(request, 'blog/edit.html', locals())
    except:
        message = '不存在该博客！'
        return render(request, 'login/index.html', locals())


def delete(request, blog_id):
    if not request.session.get('is_login', None):
        return redirect('home')
    if request.session['user_name'] != "testUser":
        return redirect('home')
    message = ''
    try:
        blog = models.Blog.objects.get(pk=blog_id)

    except:
        message = "无此博客！"
    return render(request, 'blog/delete.html', locals())


def delete_confirm(request, blog_id):
    if not request.session.get('is_login', None):
        return redirect('home')
    if request.session['user_name'] != "testUser":
        return redirect('home')
    blog = models.Blog.objects.get(pk=blog_id)
    blog.is_deleted = True
    blog.save()
    return redirect('blog:index')


def detail(request, blog_id):
    blog = models.Blog.objects.get(pk=blog_id)
    is_oldest = True
    is_newest = True
    while blog.id > 1:

        older_blog = models.Blog.objects.filter(pk=blog.id - 1).filter(is_deleted=False)
        if older_blog:
            older_blog_id = older_blog[0].id
            older_blog_name = older_blog[0].name
            is_oldest = False
            break
        else:
            blog.id = blog.id - 1
    while blog.id < models.Blog.objects.order_by('-id')[0].id:
        newer_blog = models.Blog.objects.filter(pk=blog.id + 1).filter(is_deleted=False)
        if newer_blog:
            newer_blog_id = newer_blog[0].id
            newer_blog_name = newer_blog[0].name
            is_newest = False
            break
        else:
            blog.id = blog.id + 1

    comments = models.Comment.objects.filter(blog_id=blog_id).order_by('-c_time')
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
