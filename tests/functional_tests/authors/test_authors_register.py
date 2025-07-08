from .base import AuthorsBaseTests
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class AuthorsRegisterTest(AuthorsBaseTests):
    def get_by_placeholder(self, web_element,placeholder):
        return web_element.find_element(
            By.XPATH, f'//input[@placeholder="{placeholder}"]'
        )
    
    def get_form(self):
       return self.browser.find_element(By.XPATH,'/html/body/main//div[2]/form')
    
    def fill_form_dummy_data(self,form):
        
        fields = form.find_elements(By.TAG_NAME,'input')
        for field in fields:
            if field.is_displayed():
                field.send_keys(' '*20)

    def form_field_test_with_callback(self,callback):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()

        self.fill_form_dummy_data(form)
        form.find_element(By.NAME,'email').send_keys('dummy@email.com')

        callback(form)
        return form

    def test_field_empty_first_name_error_message(self):
        def callback(form):
            first_name_field = self.get_by_placeholder(form, 'Ex: John')
            first_name_field.send_keys(' ')
            first_name_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('First name must not be empty',form.text)
        self.form_field_test_with_callback(callback=callback)

    def test_field_empty_last_name_error_message(self):
        def callback(form):
            last_name_field = self.get_by_placeholder(form, 'Ex: Smith')
            last_name_field.send_keys(' ')
            last_name_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('Last name must not be empty',form.text)
        self.form_field_test_with_callback(callback=callback)
    

    def test_field_empty_username_error_message(self):
        def callback(form):
            username_field = self.get_by_placeholder(form, 'Your user name')
            username_field.send_keys(' ')
            username_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('This field must not be empty',form.text)
        self.form_field_test_with_callback(callback=callback)
    
    def test_field_empty_email_error_message(self):
        def callback(form):
            email_field = self.get_by_placeholder(form, 'Your E-mail')
            email_field.send_keys('dummy#email')
            email_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('Informe um endereço de email válido.',form.text)
        self.form_field_test_with_callback(callback=callback)
    
    def test_field_password_do_not_match(self):
        def callback(form):
            password1 = self.get_by_placeholder(form, 'Typer your password here')
            password2 = self.get_by_placeholder(form, 'Repeat your password here')
            password1.send_keys('P@ssw0rd1')
            password2.send_keys('P@ssw0rd_different')
            password1.send_keys(Keys.ENTER)
            form = self.get_form()

            self.assertIn('Password and Repeat Password must be equals',form.text)
        self.form_field_test_with_callback(callback=callback)
    
    def test_user_valid_data_register_successfully(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()

        self.get_by_placeholder(form, 'Ex: John').send_keys('First Name')
        self.get_by_placeholder(form, 'Ex: Smith').send_keys('Last Name')
        self.get_by_placeholder(form, 'Your user name').send_keys('user_name')
        self.get_by_placeholder(form, 'Your E-mail').send_keys('email@umemail.com')
        self.get_by_placeholder(form, 'Typer your password here').send_keys('P@ssw0rd1')
        self.get_by_placeholder(form, 'Repeat your password here').send_keys('P@ssw0rd1')
        
        form.submit()

        self.assertIn('Your user is created, please log in.',
                       self.browser.find_element(By.TAG_NAME,'body').text)