from django.db import models
from users.models import AppUser
from django.shortcuts import reverse

# Create your models here.


class Recipe(models.Model):
    name = models.CharField(max_length=50)
    cooking_time = models.IntegerField(help_text="in minutes")
    ingredients = models.TextField(
        max_length=500,
        help_text="Separate ingredients with a comma and a space"
    )
    description = models.TextField(max_length=300, null=True, blank=True, default="")
    instructions = models.TextField(
        max_length=2000,
        default="",
        help_text="Number your steps and separate with a semicolon and a space, like '1. step 1; 2. step 2; 3. step 3'. Do not use semicolons within a step"
    )
    #pic = models.ImageField(upload_to="recipes", default="blank_image.png")
    pic = models.ImageField(upload_to="recipes",null=True, blank=True)
    # link to user who created the recipe (optional field)
    # if user is deleted, set field to null instead of deleting recipe
    creator = models.ForeignKey(
        AppUser, null=True, blank=True, on_delete=models.SET_NULL
    )

    # calculate difficulty of recipe based on number of ingredients and cooking time
    def calculate_difficulty(self):
        ingredients = self.ingredients.split(", ")
        if self.cooking_time < 10 and len(ingredients) < 4:
            difficulty = "Easy"
        elif self.cooking_time < 10 and len(ingredients) >= 4:
            difficulty = "Medium"
        elif self.cooking_time >= 10 and len(ingredients) < 4:
            difficulty = "Intermediate"
        elif self.cooking_time >= 10 and len(ingredients) >= 4:
            difficulty = "Hard"
        return difficulty

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("recipes:detail", kwargs={"pk": self.pk})
    
    def get_ingredients_as_list(self):
        ingredients = self.ingredients.split(", ")
        return ingredients

    def get_instructions_as_list(self):
        instructions = self.instructions.split("; ")
        return instructions