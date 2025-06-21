from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTesteBase

class RecipeViewsTests(RecipeTesteBase):

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

    def test_recipe_category_view_function_is_correct(self):
        category = reverse('recipes:category',kwargs={'category_id':1})
        view = resolve(category)
        self.assertIs(view.func,views.category) 
        
    def test_recipe_category_views_returns_404_if_no_recipes_found(self):
        view =  reverse('recipes:category',kwargs={'category_id':1000})
        response = self.client.get(view)
        self.assertEqual(response.status_code,404)
   
    def test_recipe_recipedetails_view_function_is_correct(self):
        recipe = reverse('recipes:recipe',kwargs={'id':1})
        view = resolve(recipe)
        self.assertIs(view.func,views.recipe)
    
    def test_recipe_recipedetails_views_returns_404_if_no_recipes_found(self):
        view =  reverse('recipes:recipe',kwargs={'id':1000})
        response = self.client.get(view)
        self.assertEqual(response.status_code,404)

    # def test_recipe_category_views_load_correct_templates(self):
    #     view = reverse('recipes:category',kwargs={'category_id':1})
    #     response = self.client.get(view)
    #     self.assertTemplateUsed(response,'recipes/pages/category.html')

    # def test_recipe_recipedetails_views_load_correct_templates(self):
    #     view = reverse('recipes:recipe',kwargs={'id':1})
    #     response = self.client.get(view)
    #     self.assertTemplateUsed(response,'recipes/pages/recipe-view.html')

