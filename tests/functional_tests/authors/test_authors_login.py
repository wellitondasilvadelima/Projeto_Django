from .base import AuthorsBaseTests
import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By
import time

@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTests):
    def test_user_valid_data_can_login_successfully(self):
        user_password = 'mypass'
        user = User.objects.create_user(username='myuser',password=user_password)

        self.browser.get(self.live_server_url + reverse('authors:login'))
        form = self.browser.find_element(By.CLASS_NAME,'main-form')
        username_field = self.get_by_placeholder(form,'Type your user name')
        password_field = self.get_by_placeholder(form,'Type your password')

        username_field.send_keys(user.username)
        password_field.send_keys(user_password)
        form.submit()
        time.sleep(2)
        self.assertIn(f'You aree logged in with {user.username}.',
                      self.browser.find_element(By.TAG_NAME,'body').text)