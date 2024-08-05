from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from .models import AppUser
# Django decorator for protecting FBVs
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.views.generic import DetailView


# define view that displays user profile details based on the logged in user
class ProfileView(LoginRequiredMixin, DetailView):
    model: AppUser
    template_name = "users/users_profile.html"
    context_object_name = "current_user"
    def get_object(self):
        return AppUser.objects.get(username=self.request.user)


# define function to create a new user
def signup(request):
    error_message = None
    # If sign up button is clicked
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # create new User object with the inputted username and password
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password1']
                )

                # retrieve uploaded picture and if none, use default
                pic = form.cleaned_data['pic']
                if not pic:
                    pic = 'blank-profile-picture.png'

                # create new user from AppUser model
                app_user = AppUser(
                    username=user,
                    name=form.cleaned_data['name'],
                    bio=form.cleaned_data['bio'],
                    pic=pic
                )
                # save, authenticate, and log user in
                app_user.save()
                user = authenticate(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password1']
                )
                login(request, user)
                return redirect('recipes:home')
            
            # user creation unsuccessful due to a duplicate key (username)
            except IntegrityError:
                error_message = 'An account already exists with this username'
            # all other exceptions
            except:
                error_message = 'Something went wrong.'
        # if form is not valid, don't try to create the user
        else:
            error_message = 'Something went wrong.'
    # if form submit button is not clicked
    else:
        form = SignUpForm()

    # pack up the form and appropriate error message from above scenarios
    context = {
        'form': form,
        'error_message': error_message
    }

    # load the signup.html page
    return render(request, 'users/signup.html', context)
