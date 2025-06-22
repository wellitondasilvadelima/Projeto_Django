from .test_recipe_base import RecipeTesteBase
from django.core.exceptions import ValidationError

class RecipeModelsTest(RecipeTesteBase):
    def setUp(self):
        self.recipe = self.make_recipe()
        return super().setUp()
    
    def test_recipe_title_raises_error_if_title_has_more_than_65_chars(self):
        self.recipe.title = 'A' * 70

        with self.assertRaises(ValidationError):
            self.recipe.full_clean()