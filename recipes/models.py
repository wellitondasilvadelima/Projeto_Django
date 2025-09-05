from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from collections import defaultdict
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from PIL import Image
import os

class Category(models.Model):
    name = models.CharField(max_length=65,unique=True,verbose_name=_('Category'))

    def __str__(self):
        return self.name # Isso faz com que o nome do elemento seja mostrado na aba admin category
    
    class Meta:
       verbose_name=_('Category')
       verbose_name_plural = _('Categories')

class Recipe(models.Model):
    title = models.CharField(max_length=65,verbose_name=_('title'))
    description = models.CharField(max_length=165,verbose_name=_('description'))
    slug = models.SlugField(unique=True,verbose_name=_('slug'))
    preparation_time = models.IntegerField(verbose_name=_('preparation_time'))
    preparation_time_unit = models.CharField(max_length=65,verbose_name=_('preparation_time_unit'))
    servings = models.IntegerField(verbose_name=_('servings'))
    servings_unit = models.CharField(max_length=65,verbose_name=_('servings_unit'))
    preparation_steps = models.TextField(verbose_name=_('preparation_steps')) 
    preparation_steps_is_html = models.BooleanField(default=False,verbose_name=_('preparation_steps_is_html'))
    created_at = models.DateTimeField(auto_now_add=True,verbose_name=_('created_at'))# auto_now_add = imutavel
    updated_at = models.DateField(auto_now=True,verbose_name=_('updated_at')) # auto_now mutável
    is_published = models.BooleanField(default=False,verbose_name=_('is_published'))
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d/',verbose_name=_('cover'))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True,blank=True,default='',verbose_name=_('category'))
    author = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,
                               blank=True,default=  None,verbose_name=_('author'))
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("recipes:recipe", kwargs={"id": self.id})
    
    @staticmethod
    def resize_image(image, new_width=840):
        image_full_path = os.path.join(settings.MEDIA_ROOT, image.name)
        image_pillow = Image.open(image_full_path)
        original_width, original_height = image_pillow.size

        if original_width <= new_width:
            image_pillow.close()
            return

        new_height = round((new_width * original_height) / original_width)

        new_image = image_pillow.resize((new_width, new_height), Image.LANCZOS)
        new_image.save(
            image_full_path,
            optimize=True,
            quality=50,
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.title)}'
            self.slug = slug

        saved = super().save(*args, **kwargs)

        if self.cover:
            try:
                self.resize_image(self.cover, 840)
            except FileNotFoundError:
                pass

        return saved
    
    def clean(self, *args, **kwargs):
        error_messages = defaultdict(list) 
        recipe_from_db = Recipe.objects.filter(
            title__iexact = self.title
        ).first()

        if recipe_from_db:
            if recipe_from_db.pk != self.pk:
                error_messages['title'].append(
                    'Found recipes with same title'
                )
            if error_messages:
                raise ValidationError(error_messages)
    
    class Meta:
       verbose_name=_('Recipe')
       verbose_name_plural = _('Recipes')