from django import forms
from recipes.models import Recipe
from utils.django_forms import add_attrs

class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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