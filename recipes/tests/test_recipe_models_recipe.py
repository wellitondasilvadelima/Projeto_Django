from .test_recipe_base import RecipeTesteBase,Recipe
from django.core.exceptions import ValidationError
from parameterized import parameterized

class RecipeModelsTest(RecipeTesteBase):
    def setUp(self):
        self.recipe = self.make_recipe()
        return super().setUp()
    
    def make_recipe_no_defaults(self):
        recipe = Recipe(
                        category = self.make_category(name='Test Default Category'),
                        author = self.make_author(username='newuser'),
                        title = 'Recipe title',
                        description = 'Recipe description',
                        slug = 'recipe-title-test-no-default',
                        preparation_time = 10,
                        preparation_time_unit = 'Minuts',
                        servings = 1,
                        servings_unit = 'person',
                        preparation_steps = 'descritption preparation steps',
                        cover = 'recipes/covers/2025/06/20',
                        )
        try:
            recipe.full_clean()
            recipe.save()
        except ValidationError:
             pass
        return recipe
    
    @parameterized.expand([
        ('title',65),
        ('description',165),
        ('preparation_time_unit',65),
        ('servings_unit',65),

    ])
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field,'A' * (max_length + 1 ))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
            recipe = self.make_recipe_no_defaults()
            self.assertFalse(
                 recipe.preparation_steps_is_html,
                 msg='Recipe preparation_steps_is_html is not False',
            )

    def test_recipe_published_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(
                recipe.is_published,
                msg='Recipe is_published is not False',
        )
    
    def test_recipe_string_representation(self):
         title_required = 'Testing Representation'
         title_sent = 'Testing Representation'
         self.recipe.title = title_sent
         self.recipe.full_clean()
         self.recipe.save()
         self.assertEqual(
              str(self.recipe), title_required,
              msg=f'Recipe string representation must be "{title_required}" '
                  f'but "{str(self.recipe.title)}" was recived.'
         )