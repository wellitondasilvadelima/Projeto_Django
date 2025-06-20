from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name # Isso faz com que o nome do elemento seja mostrado na aba admin category

class Recipe(models.Model):
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField()
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