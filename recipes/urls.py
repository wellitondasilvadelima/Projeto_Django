from django.urls import path
# from recipes.views import home
from . import views

app_name = 'recipes'
urlpatterns = [
    path('', views.home,name="home"),
    path('recipes/search/', views.search,name="search"),
    path('recipes/category/<int:category_id>/', views.category,name="category"),
    path('recipes/<int:id>/', views.recipe,name="recipe"),
    path('recipes/api/v1/', views.homeAPI,name="recipe_api"),
    path('recipes/api/v1/<int:id>/', views.recipedetailAPI,name="recipe_detail_api"),

]
