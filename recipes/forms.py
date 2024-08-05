#import django forms
from django import forms
from .models import Recipe
from django.forms import TextInput, NumberInput, Textarea


#define form for searching recipes
class RecipesSearchForm(forms.Form):
    recipe_name = forms.CharField(max_length=120, required=False)
    ingredient = forms.CharField(max_length=120, required=False)


#define form for creating a recipe (from Recipe model)
class CreateRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["name", "cooking_time", "ingredients", "description", "instructions", "pic"]