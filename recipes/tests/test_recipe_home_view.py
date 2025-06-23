from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTesteBase

class RecipeHomeViewTests(RecipeTesteBase):

    def test_recipe_home_view_function_is_correct(self):
        view = reverse('recipes:home')
        view = resolve(view)
        self.assertIs(view.func,views.home) # verifica a referencia entre view.func e views.home
    
    def test_recipe_home_views_returns_status_code_200_ok(self):
        view = reverse('recipes:home')
        response = self.client.get(view)
        self.assertEqual(response.status_code,200)

    def test_recipe_home_views_load_correct_templates(self):
        view = reverse('recipes:home')
        response = self.client.get(view)
        self.assertTemplateUsed(response,'recipes/pages/home.html')
    
    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        home = reverse('recipes:home')
        response = self.client.get(home)
        self.assertIn(
            'No recipes found',
            response.content.decode('utf-8')
        )
        #self.fail("terminar!")
    
    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()
        home = reverse('recipes:home')
        response = self.client.get(home)
        content = response.content.decode('utf-8')
        response_content_recipes = response.context['recipes']

        self.assertIn('Recipe title',content)
        self.assertEqual(len(response_content_recipes),1)

    def test_recipe_home_template_load_recipes_not_published(self):
        self.make_recipe(is_published=False)
        home = reverse('recipes:home')
        response = self.client.get(home)
        self.assertIn(
            'No recipes found',
            response.content.decode('utf-8')
        )