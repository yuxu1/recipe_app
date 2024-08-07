from django.urls import path, re_path
from .views import recipes_home, about_me, search_results, create_recipe, update_recipe, delete_recipe
from .views import RecipeListView, RecipeDetailView, CreatorRecipesView
from django.conf import settings
from django.views.static import serve

app_name = "recipes"

urlpatterns = [
    path("", recipes_home, name="home"),
    path("recipes/", RecipeListView.as_view(), name="recipes"),
    path("recipes/<int:pk>", RecipeDetailView.as_view(), name="detail"),
    path("search/", search_results, name="search"),
    path("create/", create_recipe, name="create_recipe"),
    path("update/<int:pk>", update_recipe, name="update_recipe"),
    path("delete/<int:pk>", delete_recipe, name="delete_recipe"),
    path("recipes/creator/<int:pk>", CreatorRecipesView.as_view(), name="creator"),
    path("about/", about_me, name="about"),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
