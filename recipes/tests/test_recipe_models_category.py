from .test_recipe_base import RecipeTesteBase
from django.core.exceptions import ValidationError

class RecipeCategoryModelsTest(RecipeTesteBase):
    def setUp(self):
        self.category = self.make_category(
            name='Category Testing'
        )
        return super().setUp()
    
    def test_recipe_category_model_name_max_length_is_65_chars(self):
        self.category.name = 'A' * 66
        with self.assertRaises(ValidationError):
            self.category.full_clean()

    def test_recipe_category_string_representation_is_name_field(self):
         self.assertEqual(
              str(self.category), self.category.name,
              msg=f'Recipe category string representation must be "{self.category}" '
                  f'but "{str(self.category.name)}" was recived.'
         )