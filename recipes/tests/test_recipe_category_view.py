from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTesteBase

class RecipeCategoryViewTests(RecipeTesteBase):
    def test_recipe_category_view_function_is_correct(self):
        category = reverse('recipes:category',kwargs={'category_id':1})
        view = resolve(category)
        self.assertIs(view.func,views.category) 
        
    def test_recipe_category_views_returns_404_if_no_recipes_found(self):
        view =  reverse('recipes:category',kwargs={'category_id':1000})
        response = self.client.get(view)
        self.assertEqual(response.status_code,404)

    def test_recipe_category_template_loads_recipes(self):
        title = 'this is a category test'
        self.make_recipe(title=title)
        view = reverse('recipes:category',kwargs={'category_id':1})
        response = self.client.get(view)
        content = response.content.decode('utf-8')

        self.assertIn(title,content)
   
    def test_recipe_category_load_recipes_not_published(self):
        self.make_recipe(is_published=False)
        view = reverse('recipes:category',kwargs={'category_id':1})
        response = self.client.get(view)
        self.assertEqual(response.status_code,404)
