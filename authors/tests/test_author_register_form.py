from unittest import TestCase
from django.test import TestCase as DjangoTesteCase
from parameterized import parameterized
from authors.forms import RegisterForm
from django.urls import reverse

class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username','Your user name'),
        ('email','Your E-mail'),
        ('first_name','Ex: John'),
        ('last_name','Ex: Smith'),
        ('password','Typer your password here'),
        ('password2','Repeat your password here'),
    ])

    def test_fields_placeholder_is_correct(self,field,placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder,placeholder)
    
    @parameterized.expand([
        ('username',(
                'Username must have letters, '
                'numbers or one os those @/./+/-/_ . '
                'The Length should be between 4 and 150 characteres.'
            )),  
        ('password',(
            'Password must be at least one uppercase letter,'
            'one lowercase letter and one number.'
            'The length should be at least 8 characters.'
            )),
        ('email','Enter a valid email address'),
    ])

    def test_fields_help_text_is_correct(self,field,helptext):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current,helptext)
    
    @parameterized.expand([
        ('username','User name'),
        ('email','E-mail'),
        ('first_name','First name'),
        ('last_name','Last name'),
        ('password','Password'),
        ('password2','Repeat password'),
    ])
    def test_fields_label_is_correct(self,field,label):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(current,label)

class AuthorRegisterFormIntegrationTest(DjangoTesteCase):
    def setUp(self,*args, **kwargs):
        self.form_data = {
            'first_name':'first',
            'last_name':'last',
            'username':'user',
            'email':'email@email.com',
            'password': 'Str0ngP@ssword',
            'password2':'Str0ngP@ssword',
        }
        return super().setUp(*args, **kwargs)
    
    @parameterized.expand([
        ('username','This field must not be empty'),
        ('first_name','First name must not be empty'),
        ('last_name','Last name must not be empty'),
        ('password','This field must not be empty'),
        ('password2','Password is not the same, please repeat the password'),
        ('email','E-mail is required'),
    ])

    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url,data=self.form_data,follow=True)#follow = True para que o caminho sejaseguido pelo redirecionamento.
        
        self.assertIn(msg,response.content.decode('utf-8'))
        self.assertIn(msg,response.context['form'].errors.get(field))
    
    def test_username_field_min_length_should_be_4(self):
        self.form_data['username'] = 'joa'
        url = reverse('authors:create')
        response = self.client.post(url,data=self.form_data,follow=True)#follow = True para que o caminho sejaseguido pelo redirecionamento.
        msg = 'Username must have at least 4 characters'

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))


    def test_username_field_max_length_should_be_150(self):
        self.form_data['username'] = 'A' * 151
        url = reverse('authors:create')
        response = self.client.post(url,data=self.form_data,follow=True)#follow = True para que o caminho sejaseguido pelo redirecionamento.
        
        msg = 'Username must have at less than 150 characters'

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))
    
    def test_password_field_is_valid(self):
        self.form_data['password'] = 'ABC123'
        url = reverse('authors:create')
        response = self.client.post(url,data=self.form_data,follow=True)#follow = True para que o caminho sejaseguido pelo redirecionamento.
        
        msg = 'Passoword invalid!'

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))

        self.form_data['password'] = '1Sd#$0zx'
        url = reverse('authors:create')
        response = self.client.post(url,data=self.form_data,follow=True)#follow = True para que o caminho sejaseguido pelo redirecionamento.
        
        msg = 'Passoword invalid!'

        self.assertNotIn(msg, response.content.decode('utf-8'))
        #self.assertNotIn(msg, response.context['form'].errors.get('password'))
    
    def test_password_end_password_confirmation_are_equal(self):
        self.form_data['password'] = '1Sd#$0zx'
        self.form_data['password2'] = '1Sd#$0zz'
        url = reverse('authors:create')
        response = self.client.post(url,data=self.form_data,follow=True)#follow = True para que o caminho sejaseguido pelo redirecionamento.

        msg = 'Password and Repeat Password must be equals'
        
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))

        self.form_data['password'] = '1Sd#$0zx'
        self.form_data['password2'] = '1Sd#$0zx'
        url = reverse('authors:create')
        response = self.client.post(url,data=self.form_data,follow=True)#follow = True para que o caminho sejaseguido pelo redirecionamento.

        msg = 'Password and Repeat Password must be equals'
        
        self.assertNotIn(msg, response.content.decode('utf-8'))

 
    def test_send_get_request_to_registration_create_view_returns_404(self):
        url = reverse('authors:create')
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)
    
   
    def test_email_field_must_be_unique(self):
        url = reverse('authors:create')
        # self.form_data['email'] = 'email@email.com'
        self.client.post(url,data=self.form_data,follow=True)
        response = self.client.post(url,data=self.form_data,follow=True)

        msg = 'User e-mail already in use'
        #msg = 'Enter a valid email address'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('email'))