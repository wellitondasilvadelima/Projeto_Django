from .base import RecipeBaseFunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest
from unittest.mock import patch
import time

@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_Page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME,'body')
        self.assertIn('No recipes found', body.text)
    
    @patch('recipes.views.PER_PAGE', new = 2)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch()
        title_required = recipes[0].title

        self.browser.get(self.live_server_url)
        search_input = self.browser.find_element(By.XPATH,'//input[@placeholder="Search for a recipe"]')
        search_input.send_keys(title_required)
        search_input.send_keys(Keys.ENTER) 
        time.sleep(6)
        body = self.browser.find_element(By.CLASS_NAME,'main-content-list')
        self.assertIn(title_required,body.text)
