from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from posts_app.models import Post


class Comment(models.Model):
    comment_name = models.CharField(max_length=150, verbose_name='Nome')
    comment_email = models.EmailField(verbose_name='E-mail')
    comment = models.TextField(verbose_name='Comentário')
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, blank=True, null=True)
    comment_date = models.DateTimeField(default=timezone.now)
    comment_published = models.BooleanField(default=False)

    def __str__(self):
        return self.comment_name
