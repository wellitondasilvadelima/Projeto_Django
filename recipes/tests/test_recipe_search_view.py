from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTesteBase

class RecipeSearchViewsTests(RecipeTesteBase):
    def test_recipe_search_uses_correct_view_function(self):
        url = reverse('recipes:search')
        resolved = resolve(url)
        self.assertEqual(resolved.func,views.search)
    
    def test_recipe_search_loads_correct_template(self):
        url = reverse('recipes:search') + "?q=teste"
        response = self.client.get(url)
        self.assertTemplateUsed(response,'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        url = reverse('recipes:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse('recipes:search') + '?q=<Teste>'
        response = self.client.get(url)
        msg = "Procurar por"
        self.assertIn(
            msg +' &quot;&lt;Teste&gt;&quot;',
            response.content.decode('utf-8')
        )

    def test_recipe_search_can_find_recipe_by_title(self):
        title_one  = 'This is title one'
        title_two  = 'This is title two'
        title_both = 'This is title'

        recipe_one = self.make_recipe(
            slug='recipe-one', title=title_one,
            author_data={'username':'one'}
        )
        recipe_two = self.make_recipe(
            slug='recipe-two',title=title_two,
            author_data={'username':'two'}
        )

        url = reverse('recipes:search')
        response_one = self.client.get(f'{url}?q={title_one}')
        response_two = self.client.get(f'{url}?q={title_two}')
        response_both = self.client.get(f'{url}?q={title_both}')

        self.assertIn(recipe_one, response_one.context['recipes'])
        self.assertNotIn(recipe_two, response_one.context['recipes'])

        self.assertIn(recipe_two, response_two.context['recipes'])
        self.assertNotIn(recipe_one, response_two.context['recipes'])

        self.assertIn(recipe_one, response_both.context['recipes'])
        self.assertIn(recipe_two, response_both.context['recipes'])