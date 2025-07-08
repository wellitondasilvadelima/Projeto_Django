from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.django_forms import add_placeholder,strong_password

class RegisterForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'],'Your user name')
        add_placeholder(self.fields['email'],'Your E-mail')
        add_placeholder(self.fields['first_name'],'Ex: John')
        add_placeholder(self.fields['last_name'],'Ex: Smith')
        add_placeholder(self.fields['password'],'Typer your password here')
        add_placeholder(self.fields['password2'],'Repeat your password here')
   
    first_name =  forms.CharField(
        required=True,
        error_messages = {
            'required':'First name must not be empty'
        },
        label='First name',
        
    )

    last_name =  forms.CharField(
        required=True,
        error_messages = {
            'required':'Last name must not be empty',
        },
        label='Last name',
    )
        
    email =  forms.CharField(
        required=True,
        error_messages = {
            'required':'E-mail is required',
        },
        help_text='Enter a valid email address',
        label='E-mail',
    )

    username =  forms.CharField(
        required=True,
        error_messages = {
            'required':'This field must not be empty',
            'min_length': 'Username must have at least 4 characters',
            'max_length': 'Username must have at less than 150 characters',
        },
        help_text=(
            'Username must have letters, '
            'numbers or one os those @/./+/-/_ . '
            'The Length should be between 4 and 150 characteres.'
        ), 
        label='User name',
        min_length=4, max_length=150,
    )

    password2 =  forms.CharField(
        required=True,
        widget = forms.PasswordInput(),
        error_messages = {
            'required':'Password is not the same, please repeat the password'
        },
        label='Repeat password',
        
    )

    password =  forms.CharField(
        required=True,
        widget = forms.PasswordInput(),
        error_messages = {
            'required':'This field must not be empty'
        },
        label='Password',
        help_text='Password must be at least one uppercase letter,'
                'one lowercase letter and one number.'
                'The length should be at least 8 characters.',
        validators=[strong_password],
    )
    
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password'
        ]

        labels = {
            'last_name':'Last name',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email','')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError('User e-mail already in use',code='invalid')

        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if (password != password2):
            password_confirmation_error = ValidationError(
                'Password and Repeat Password must be equals',
                code='invalid',
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'password2':[
                    password_confirmation_error,
                    'Enter a new password again',        
                ],
            })

# Exemple CODES :
        #fields = '__all__' # para o fjangpo criar os campos de acordo com o model
        # exclude = ['last_name']

        # labels = {
        #     'username':'User name',
        #     'last_name':'Last name',
        # }

        # error_messages = {
        #     'username':{
        #         'required':'This field must not be empty'
        #     },
        # }
        # help_texts={
        #     'email':'Enter a valid email address',
        # }
        # widgets = {
        #     'password':forms.PasswordInput(
        #         attrs={'placeholder': 'Typer your password here'}
        #         )     
        # }

    # def clean_password(self):
    #     data = self.cleaned_data.get('password')

    #     if 'atenção' in data:
    #         raise ValidationError(
    #             'Do not enter %(value)s in the password field',
    #             code='invalid',
    #             params={'value':'"atenção"'},
    #         )


    # def clean_first_name(self):
    #     data = self.cleaned_data.get('first_name')

    #     if 'John Smith' in data:
    #         raise ValidationError(
    #             'Não digite %(value)s no campo First Name',
    #             code='invalid',
    #             params={'value':'John Smith'}
    #         )
