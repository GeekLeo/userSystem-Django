from django.shortcuts import render, redirect
from . import forms
from . import models


# Create your views here.

def index(request):
    blog_list = models.Blog.objects.order_by('c_time')
    return render(request, 'blog/index.html', locals())


def create(request):
    if not request.session.get('is_login', None):
        return redirect('index')
    if request.session['user_name'] != "testUser":
        return redirect('index')
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
