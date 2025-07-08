from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.options import Options
import os
from recipes.tests.test_recipe_base import RecipeMixin

class RecipeBaseFunctionalTest(StaticLiveServerTestCase,RecipeMixin):
    def setUp(self):
        headless = os.environ.get('SELENIUM_HEADLESS') == '1'    

        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')

        self.browser = webdriver.Chrome(options=chrome_options)
        return super().setUp()
    
    def tearDown(self):
        self.browser.quit()
        return super().tearDown()
    
