from django import forms
from recipes.models import Recipe
from utils.django_forms import add_attrs
from collections import defaultdict
from django.core.exceptions import ValidationError
from utils.strings import is_positive_number 

class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__erros_form = defaultdict(list)

        add_attrs(self.fields.get('preparation_steps'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = 'title', 'description', 'preparation_time','preparation_time_unit', 'servings', 'servings_unit', 'preparation_steps', 'cover'
        widgets = {
            'cover' : forms.FileInput(
                attrs={
                    'class':'span-2',
                    }
            ),

            'servings_unit': forms.Select(
                choices=(
                            ('Porção','Proção'),
                            ('Porções','Proções'),
                            ('Fatias','Fatias'),
                            ('Pessoas','Pessoas'),
                         ),
            ),

            'preparation_time_unit': forms.Select(
                choices=(
                            ('Minutos','Minutos'),
                            ('Horas','Horas'),
                        ),
            ),
        }
    
    def clean(self, *args, **kwargs):
        super_clear = super().clean(*args, **kwargs)

        clean_data = self.cleaned_data

        title = clean_data.get('title')
        description = clean_data.get('description')

        if len(title) < 5:
            self.__erros_form['title'].append(
                'Title must have at least 5 chars.'
            )
        
        if title == description:
            self.__erros_form['title'].append('Cannot be equal to description')
            self.__erros_form['description'].append('Cannot be equal to title')

        if self.__erros_form:
            raise ValidationError(self.__erros_form)
        
        return super_clear
    
     
    def clean_preparation_time(self):
        field_name = 'preparation_time'
        value = self.cleaned_data.get(field_name)

        if not is_positive_number(value):
             self.__erros_form[field_name].append(
                    'Must be a positive number'
                 )
             
        return field_name
    
    def clean_servings(self):
        field_name = 'servings'
        value = self.cleaned_data.get(field_name)

        if not is_positive_number(value):
             self.__erros_form[field_name].append(
                 'Must be a positive number'
                 )
             
        return field_name