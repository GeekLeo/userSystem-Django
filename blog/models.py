from django.db import models
from django.utils import timezone


# Create your models here.

class Blog(models.Model):
    name = models.CharField(max_length=255, unique=True)
    summary = models.TextField()
    content = models.TextField()
    c_time = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    # user = models.ForeignKey('login.User', on_delete=models.CASCADE)
    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "博客"
        verbose_name_plural = "博客"


class Comment(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField()
    c_time = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    blog = models.ForeignKey('blog.Blog', on_delete=models.CASCADE)
    user = models.ForeignKey('login.User', on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE)

    def __str__(self):
        return self.blog.name + " UserName:" + self.user.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "评论"
        verbose_name_plural = "评论"
