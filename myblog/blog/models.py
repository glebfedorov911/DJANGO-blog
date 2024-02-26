from PIL import Image
from django.db import models

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.urls import reverse

from uuid import uuid4
from pytils.translit import slugify

from .managers import UserManager

def unique_slugify(instance, slug):
    model = instance.__class__
    unique_slug = slugify(slug)
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{unique_slug}-{uuid4().hex[:8]}'
    return unique_slug

class User(AbstractBaseUser, PermissionsMixin):
    COUNTRY = (
        ("RUS", "Russia"),
        ("UK", "United Kingdom"),
        ("US", "United States"),
        ("OTH", "Other")
    )

    email = models.EmailField(blank=False, null=False, unique=True)
    phone = models.CharField(max_length=30, blank=False, null=False, unique=True)
    county = models.CharField(max_length=3, choices=COUNTRY)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['phone']

    def __str__(self):
        return f"-=-=-=-email: {self.email}-=-=-=-"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        unique_together = ('email', 'phone')



class Article(models.Model):
    name = models.CharField(max_length=100, unique=True)
    desc = models.TextField()
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    img = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('article', kwargs={'article_slug': self.slug})

    def save(self, *args, **kwargs):
        self.save_slug(*args, **kwargs)
        self.save_img(*args, **kwargs)

    def save_slug(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)

    def save_img(self, *args, **kwargs):
        super().save(*args, **kwargs)
        standart = (250, 350)

        img = Image.open(self.img)
        width_photo, height_photo = img.size
        if width_photo > standart[0] or height_photo > standart[0]:
            img.thumbnail(standart)

        img.save(self.img.path, 'PNG')
        img.close()

    class Meta:
        verbose_name = "Статьи"
        verbose_name_plural = "Статья"

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    msg = models.TextField()

    def __str__(self):
        return f'self.author.email'

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"