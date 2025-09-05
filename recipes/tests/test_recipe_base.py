from django.test import TestCase
from recipes import views
from recipes.models import Category,Recipe,User

class RecipeMixin():
      
    def make_category(self,name='Category'):
        category, _ = Category.objects.get_or_create(name=name)
        return  category

    def make_author(
                self,
                first_name='User',
                last_name='Name',
                username='username',
                password='asdf1234',
                email='user@email.com',    
                ):
        return  User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    password=password,
                    email=email,
                    )
    def make_recipe(
            self,
            category_data = None,
            author_data = None,
            title = 'Recipe title',
            description = 'Recipe description',
            slug = 'recipe-title',
            preparation_time = 10,
            preparation_time_unit = 'Minuts',
            servings = 1,
            servings_unit = 'person',
            preparation_steps = 'descritption preparation steps',
            preparation_steps_is_html = False ,
            is_published = True,
            cover = 'recipes/covers/2025/06/20',
            ):
            if(category_data is None):
                    category_data = {}
            if(author_data is None):
                author_data = {}

            return Recipe.objects.create(
                    category = self.make_category(**category_data),
                    author = self.make_author(**author_data),
                    title = title,
                    description = description,
                    slug = slug,
                    preparation_time = preparation_time,
                    preparation_time_unit = preparation_time_unit,
                    servings = servings,
                    servings_unit = servings_unit,
                    preparation_steps = preparation_steps,
                    preparation_steps_is_html = preparation_steps_is_html ,
                    is_published = is_published,
                    cover = cover,
                    )
    
    def make_recipe_in_batch(self,qnt=10):
        recipes = []
        for i in range(qnt):
            kwargs = {
                 'title':f'Recipe Title {i}',
                 'slug':f'r{i}',
                 'author_data':{'username':f'u{i}'}}
            recipe = self.make_recipe(**kwargs)
            recipes.append(recipe)
        
        return recipes


class RecipeTesteBase(TestCase,RecipeMixin):
    def setUp(self):
        return super().setUp()
   