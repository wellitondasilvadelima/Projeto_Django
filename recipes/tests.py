from django.test import TestCase
from django.urls import reverse, resolve

from recipes import views

class RecipeURLsTest(TestCase):
    def test_recipe_home_url_is_correct(self):
       home_url = reverse('recipes:home')
       self.assertEqual(home_url,'/')

    def test_recipe_category_url_is_correct(self):
        url = reverse('recipes:category',kwargs={'category_id':1})
        self.assertEqual(url,'/recipes/category/1/')

    def test_recipe_recipedetails_url_is_correct(self):
        url = reverse('recipes:recipe',kwargs={'id':1})
        self.assertEqual(url,'/recipes/1/')

class RecipeViewsTests(TestCase):
    def test_recipe_home_view_function_is_correct(self):
        home = reverse('recipes:home')
        view = resolve(home)
        self.assertIs(view.func,views.home) # verifica a referencia entre view.func e views.home
    
    def test_recipe_category_view_function_is_correct(self):
        category = reverse('recipes:category',kwargs={'category_id':1})
        view = resolve(category)

        self.assertIs(view.func,views.category) 
   
    def test_recipe_recipedetails_view_function_is_correct(self):
        recipe = reverse('recipes:recipe',kwargs={'id':1})
        view = resolve(recipe)
        self.assertIs(view.func,views.recipe) 