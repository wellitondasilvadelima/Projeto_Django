from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from collections import defaultdict
from django.core.exceptions import ValidationError

class Category(models.Model):
    name = models.CharField(max_length=65,unique=True)

    def __str__(self):
        return self.name # Isso faz com que o nome do elemento seja mostrado na aba admin category

class Recipe(models.Model):
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField() 
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)# auto_now_add = imutavel
    updated_at = models.DateField(auto_now=True) # auto_now mutável
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True,blank=True,default='')
    author = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,
                               blank=True,default=  None)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("recipes:recipe", kwargs={"id": self.id})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.title)}'
            self.slug = slug

        return super().save(*args, **kwargs)
    
    def clean(self, *args, **kwargs):
        error_messages = defaultdict(list) 
        recipe_from_db = Recipe.objects.filter(
            title_iexact = self.title
        ).first()

        if recipe_from_db:
            if recipe_from_db.pk != self.pk:
                error_messages['title'].append(
                    'Found recipes with same title'
                )
            if error_messages:
                raise ValidationError(error_messages)