from django.test import TestCase, Client
from .models import Recipe, AppUser
from .forms import RecipesSearchForm, CreateRecipeForm
from django.urls import reverse
from django.contrib.auth.models import User

# Create your tests here.


# Test recipe model
class RecipeModelTest(TestCase):
    # Set up non-modified objects used by all test methods
    def setUpTestData():
        Recipe.objects.create(
            name="Tea",
            cooking_time=5,
            ingredients="Tea Leaves, Sugar, Water",
            instructions="Step 1; Step 2"
        )

    # test whether the recipe's name is initialized as expected
    def test_recipe_name(self):
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    # test whether the recipe name's max length is 50 as set
    def test_recipe_name_max_length(self):
        recipe = Recipe.objects.get(id=1)
        max_length = recipe._meta.get_field("name").max_length
        self.assertEqual(max_length, 50)

    # test whether the cooking time is valid (an integer)
    def test_cooking_time_is_integer(self):
        recipe = Recipe.objects.get(id=1)
        cooking_time = recipe.cooking_time
        self.assertIs(
            type(cooking_time), int, "cooking_time needs to be a whole number"
        )

    # test whether the cooking_time help text is displayed as expected
    def test_cooking_time_help_text(self):
        recipe = Recipe.objects.get(id=1)
        help_text = recipe._meta.get_field("cooking_time").help_text
        self.assertEqual(help_text, "in minutes")

    # test whether the ingredients field's max length is 500 as set
    def test_ingredients_max_length(self):
        recipe = Recipe.objects.get(id=1)
        max_length = recipe._meta.get_field("ingredients").max_length
        self.assertEqual(max_length, 500)

    # test whether the ingredients help text is displayed as expected
    def test_ingredients_help_text(self):
        recipe = Recipe.objects.get(id=1)
        help_text = recipe._meta.get_field("ingredients").help_text
        self.assertEqual(
            help_text, "Separate ingredients with a comma and a space")

    # test whether the difficulty is calculated correctly
    def test_calculate_difficulty(self):
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.calculate_difficulty(), "Easy")

    # test whether the description field's max length is 300 as set
    def test_description_max_length(self):
        recipe = Recipe.objects.get(id=1)
        max_length = recipe._meta.get_field("description").max_length
        self.assertEqual(max_length, 300)

    # test whether the recipe image is set to the default if none is uploaded by user
    def test_recipe_image_default(self):
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.pic, "blank_image.png")

    # test whether get_absolute_url takes user to detail page of recipe#1
    def test_get_absolute_url(self):
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.get_absolute_url(), "/recipes/1")

    # test whether ingredients are returned as a list
    def test_get_ingredients_as_list(self):
        recipe = Recipe.objects.get(id=1)
        ingredients_list = recipe.get_ingredients_as_list()
        self.assertTrue(type(ingredients_list) == list)
        self.assertEqual(len(ingredients_list), 3)

    # test whether instructions are correctly returned as a list
    def test_get_instructions_list(self):
        recipe = Recipe.objects.get(id=1)
        instructions_list = recipe.get_instructions_as_list()
        self.assertTrue(type(instructions_list) == list)
        self.assertEqual(len(instructions_list), 2)

    # test whether instructions max length is correct
    def test_instructions_max_length(self):
        recipe = Recipe.objects.get(id=1)
        max_len = recipe._meta.get_field("instructions").max_length
        self.assertEqual(max_len, 2000)

    # test whether instructions help text is correct
    def test_instructions_help_text(self):
        recipe = Recipe.objects.get(id=1)
        text = recipe._meta.get_field("instructions").help_text
        self.assertEqual(
            text, "Number your steps and separate with a semicolon and a space, like '1. step 1; 2. step 2; 3. step 3'. Do not use semicolons within a step")


# Test recipe search form and create recipe form
class RecipeFormsTest(TestCase):

    def test_recipes_search_form_by_name(self):
        form_data = {'recipe_name': 'test', 'ingredient': ''}
        form = RecipesSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_recipes_search_form_by_ingredient(self):
        form_data = {'recipe_name': '', 'ingredient': 'test ingredient 2'}
        form = RecipesSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_recipes_search_form_fields_valid(self):
        form_data = {'recipe_name': 'test', 'ingredient': 'test ingredient 2'}
        form = RecipesSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_create_recipe_form(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        form_data = {
            'name': 'Test Recipe',
            'cooking_time':24,
            'ingredients':'Ingredient 1, Ingredient 2',
            'description': 'This is a test recipe.',
            'instructions': '1. Step 1; 2. Step 2; 3. Step 3',
            'pic': 'test_pic.jpg',
            'creator': user,
        }
        form = CreateRecipeForm(data=form_data)
        self.assertTrue(form.is_valid())


# Test authentication of views and redirecting
class RecipeViewsAuthTest(TestCase):
    # set up test recipe and test user
    def setUpTestData():
        Client()
        user = User.objects.create_user(
            username='testuser', password='testpassword')
        AppUser.objects.create(username=user, name="Test User", bio="test bio")
        Recipe.objects.create(
            name='Test Recipe',
            cooking_time=25,
            ingredients='Test Ingredient 1, Test Ingredient 2, Test Ingredient 3',
            description='this is a simple test recipe',
            instructions='Step 1, Step 2, Step 3, Step 4, Step 5',
            creator=AppUser.objects.get(id=1)
        )

    # test whether home(welcome) page is accessible to everyone
    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipes_home.html')

    # test whether recipes list view redirects when unauthorized
    def test_login_required_for_list_view(self):
        response = self.client.get(reverse('recipes:recipes'))
        self.assertRedirects(response, '/login/?next=/recipes/')

    # test whether recipes details view redirects when unauthorized
    def test_login_required_for_details_view(self):
        recipe = Recipe.objects.get(id=1)
        response = self.client.get(reverse('recipes:detail', args=[recipe.id]))
        self.assertRedirects(response, f'/login/?next=/recipes/{recipe.id}')

    # test whether recipes search redirects when unauthorized
    def test_login_required_for_recipes_search(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertRedirects(response, '/login/?next=/search/')

    # test whether user profile view redirects when unauthorized
    def test_login_required_for_profile(self):
        response = self.client.get(reverse('users:profile'))
        self.assertRedirects(response, '/login/?next=/profile/')

    # test whether recipes list view is accessible when authorized
    def test_list_view_access_with_auth(self):
        login = self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('recipes:recipes'))
        self.assertTrue(login)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipes_list.html')

    # test whether recipes details view is accessible when authorized
    def test_details_view_access_with_auth(self):
        login = self.client.login(username='testuser', password='testpassword')
        recipe = Recipe.objects.get(id=1)
        response = self.client.get(reverse('recipes:detail', args=[recipe.id]))
        self.assertTrue(login)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipes_details.html')

    # test whether user profile view is accessible when authorized
    def test_profile_view_access_with_auth(self):
        login = self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('users:profile'))
        self.assertTrue(login)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/users_profile.html')

    # test whether recipes search is accessible when authorized
    def test_recipes_search_access_with_auth(self):
        login = self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('recipes:search'))
        self.assertTrue(login)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/search_results.html')

    def test_creator_redirect_with_auth(self):
        login = self.client.login(username='testuser', password='testpassword')
        recipe = Recipe.objects.get(id=1)
        response = self.client.get(reverse('recipes:creator', args=[recipe.id]))
        self.assertTrue(login)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/creator_recipes.html')

    def test_about_me_page_access(self):
        response=self.client.get(reverse('recipes:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/about_me.html')