from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from time import time
from django.utils.text import slugify

def gen_slug(s):
    new_slug = slugify(s)
    if len(new_slug) > 30:
        new_slug = new_slug[:30]
    return new_slug+'-'+str(int(time()))

class Post(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="author")
    title = models.CharField(max_length=255)
    body = models.TextField()
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    image = models.ImageField(blank=True)
    date_pub = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_pub"]

    def __str__(self):
        return f"{self.author}, {self.title}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('post_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('post_delete_url', kwargs={'slug': self.slug})


class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_comment")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_comment")
    date = models.DateTimeField(auto_now_add=True)
    comment_text = models.CharField(max_length=500)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.author} {self.comment_text}"

    def get_delete_url(self):
        return reverse('comment_delete_url', kwargs={'pk': self.pk})
