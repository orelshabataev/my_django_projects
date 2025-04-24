from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата корректировки")
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")
    slug = models.SlugField(max_length=200, verbose_name="Slug", unique=True)
    content = models.TextField(verbose_name="Контент")
    photo = models.ImageField(upload_to='posts/%Y/%m/%d/', verbose_name="Фото", blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, verbose_name="Категория")

    auther = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='posts', null=True, default=None)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={'slug_name': self.slug})

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Категория', blank=False)
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField("Текст комментария")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Коментарий от {self.author.username}"




