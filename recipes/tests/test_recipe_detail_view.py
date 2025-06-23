from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTesteBase

class RecipeDetailViewTests(RecipeTesteBase):
    def test_recipe_recipedetails_view_function_is_correct(self):
        recipe = reverse('recipes:recipe',kwargs={'id':1})
        view = resolve(recipe)
        self.assertIs(view.func,views.recipe)
    
    def test_recipe_recipedetails_views_returns_404_if_no_recipes_found(self):
        view =  reverse('recipes:recipe',kwargs={'id':1000})
        response = self.client.get(view)
        self.assertEqual(response.status_code,404)
    
    def test_recipe_recipedetails_template_load_is_correct(self):
        title = 'this is a details page test - It a load one recipe'
        # Nedd a recipe for this test
        self.make_recipe(title=title)
        view = reverse('recipes:recipe',kwargs={'id':1})
        response = self.client.get(view)
        content = response.content.decode('utf-8')

        self.assertIn(title,content)
    
    def test_recipe_recipedetails_template_load_recipes_not_published(self):
        self.make_recipe(is_published=False)
        view = reverse('recipes:recipe',kwargs={'id':1})
        response = self.client.get(view)
        self.assertEqual(response.status_code,404)
