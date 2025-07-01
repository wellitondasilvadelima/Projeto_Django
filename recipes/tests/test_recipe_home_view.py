from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTesteBase
from unittest.mock import patch

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

    def test_recipe_home_is_paginated(self):
        for i in range(9):
            kwargs = {'slug':f'r{i}','author_data':{'username':f'u{i}'}}
            self.make_recipe(**kwargs)

        with patch('recipes.views.PER_PAGE',new=3):
            home = reverse('recipes:home')
            response = self.client.get(home)
            recipes = response.context['recipes']
            paginator = recipes.paginator

        self.assertEqual(paginator.num_pages,3)
        self.assertEqual(len(paginator.get_page(1)),3)
        self.assertEqual(len(paginator.get_page(2)),3)
        self.assertEqual(len(paginator.get_page(3)),3)

    def test_page_param_invalid(self):
        view = reverse('recipes:home') + '?page=abc'
        response = self.client.get(view)
        recipes = response.context['recipes']
        paginator = recipes.paginator

        self.assertEqual(response.status_code,200) 
        self.assertEqual(paginator.num_pages,1)
