from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import AppUser
from django.urls import reverse
from .forms import SignUpForm

# Create your tests here.


class UserModelTest(TestCase):
    # Set up non-modified objects used by all test methods
    def setUpTestData():
        user = User.objects.create_user(username="yufanx8", password="testpassword")
        AppUser.objects.create(username=user, name="Yufan Xu", bio="sample bio")

    def test_user_name(self):
        user = AppUser.objects.get(id=1)
        field_label = user._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_user_name_max_length(self):
        user = AppUser.objects.get(id=1)
        max_length = user._meta.get_field("name").max_length
        self.assertEqual(max_length, 50)

    def test_user_bio_max_length(self):
        user = AppUser.objects.get(id=1)
        max_length = user._meta.get_field("bio").max_length
        self.assertEqual(max_length, 1000)

    # Check whether the user picture is set to the default when no custom picture is uploaded
    def test_user_pic_default(self):
        user = AppUser.objects.get(id=1)
        self.assertEqual(user.pic, "blank-profile-picture.png")


class UserAuthTest(TestCase):
    def setUpTestData():
        Client()
        user = User.objects.create_user(username='testuser', password='testpassword')
        AppUser.objects.create(
            username = user,
            name = 'testuser',
            bio='Test bio - placeholder'
        )

    def test_profile_redirect_without_auth(self):
        response = self.client.get(reverse('users:profile'))
        self.assertRedirects(response, f'/login/?next={reverse("users:profile")}')

    def test_profile_redirect_with_auth(self):
        login = self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('users:profile'))
        self.assertTrue(login)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/users_profile.html')

    def test_signup_accessible(self):
        response = self.client.get(reverse('users:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/signup.html')


class SignUpFormTest(TestCase):
    def test_signup_form_valid(self):
        form_data = {
            'username': 'TestUser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'name': 'Test User Name',
            'bio': 'Test Bio',
            'pic': ''
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid)