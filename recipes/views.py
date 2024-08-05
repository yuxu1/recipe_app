from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Recipe, AppUser
from django.contrib.auth.mixins import LoginRequiredMixin #to protect class-based views
from django.contrib.auth.decorators import login_required #to protect function-based views
from .forms import RecipesSearchForm, CreateRecipeForm
import pandas as pd
from .utils import get_pie_chart, get_bar_chart
from users.models import User


def recipes_home(request):
    return render(request, "recipes/recipes_home.html")


def about_me(request):
    return render(request, 'recipes/about_me.html')


# class-based view-recipes list
class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = "recipes/recipes_list.html"


# class-based view - recipe details
class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = "recipes/recipes_details.html"


# function-based view - search/filter recipes
@login_required
def search_results(request):
    #create an instance of RecipesSearchForm
    form = RecipesSearchForm(request.POST or None)
    #initialize a DataFrame object as None
    recipes_df = None
    recipes_dict = None
    #initialize 2 chart variables to None
    pie_chart = None
    bar_chart = None

    #check if search button is clicked
    if request.method == 'POST':
        #read input
        recipe_name = request.POST.get('recipe_name')
        search_ingredient = request.POST.get('ingredient')

        #apply filter to extract data as a QuerySet
        #if only recipe name is inputted, filter by name
        if recipe_name and not search_ingredient:
            qs = Recipe.objects.filter(name__icontains=recipe_name)
        #if only ingredient is inputted, filter by ingredient
        elif search_ingredient and not recipe_name:
            qs = Recipe.objects.filter(ingredients__icontains=search_ingredient)
        #if both search fields are inputted, apply both filters
        elif recipe_name and search_ingredient:
            qs = Recipe.objects.filter(name__icontains=recipe_name, ingredients__icontains=search_ingredient)

        #if data is found
        if qs:
            #convert queryset values to a pandas DataFrame
            recipes_df = pd.DataFrame(qs.values())
            difficulty_values = []
            #for each recipe in filtered queryset
            for obj in qs:
                diff = obj.calculate_difficulty() #calculate recipe's difficulty
                difficulty_values.append(diff) #append to list
            recipes_df['difficulty'] = difficulty_values #add list as new 'difficulty' column in queryset

            bar_chart = get_bar_chart(recipes_df)
            pie_chart = get_pie_chart(recipes_df)
            #convert DataFrame to dictionary
            recipes_dict = recipes_df.to_dict(orient='records')

    #pack up data to be sent to template in context dictionary
    context = {
        'form':form,
        'recipes_df': recipes_df,
        'recipes_dict': recipes_dict,
        'pie_chart': pie_chart,
        'bar_chart': bar_chart,
    }

    #load the recipes/search_results.html page using the data prepared
    return render(request, 'recipes/search_results.html', context)


# function-based view - create a recipe (any user)
@login_required
def create_recipe(request):
    #if submit button is clicked
    if request.method == 'POST':
        #create a form to add a recipe
        form = CreateRecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            #set the "creator" as the current signed-in user
            recipe.creator = AppUser.objects.get(username=request.user)
            recipe.save()
        else:
            print("Something went wrong.")
    else:
        form = CreateRecipeForm()
    #redirect user to all recipes page after successfully creating new recipe
    return redirect('recipes:recipes')


# function-based view - update a recipe (only the creator of the recipe)
@login_required
def update_recipe(request, pk):
    #retrieve recipe object with primary key of pk in parameter
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        #create form to change an existing Recipe object w/ matching primary key
        form = CreateRecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            recipe.save()
            return redirect('recipes:detail', pk=recipe.pk)
        else:
            form = CreateRecipeForm(instance=recipe)
            print("Something went wrong.")
    
    return render(request, 'recipes/recipes_details.html', {'object': recipe})


# function-based view - delete a recipe (only the creator of the recipe)
@login_required
def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    recipe.delete()
    return redirect('recipes:recipes')


#define view to display a creator(user) and their recipes
class CreatorRecipesView(LoginRequiredMixin, DetailView):
    model = AppUser
    template_name = 'recipes/creator_recipes.html'

    #retrieve user that is selected 
    def get_queryset(self):
        return AppUser.objects.filter(pk=self.kwargs['pk'])
    
    
    #override default DetailView to add information about the user's recipes
    def get_context_data(self, **kwargs):
        #call base implementation first to get a context
        context = super().get_context_data(**kwargs)
        #add in a QuerySet of all recipes created by the selected user
        context['recipes'] = Recipe.objects.filter(creator = self.object)
        return context