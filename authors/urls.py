from django.urls import path
from . import views

app_name = 'authors'
urlpatterns = [
    path('register/', views.register_view,name='register'),
    path('register/create/', views.register_create,name='register_create'),
    path('login/', views.login_view,name='login'),
    path('login/create/', views.login_create,name='login_create'),
    path('logout/', views.logout_view,name='logout'),
    path('dashboard/', views.dashboard_view,name='dashboard'),

    path('dashboard/recipe/new/', views.recipe_new_view,name='recipe_new'),

    path('dashboard/recipe/delete/', 
         views.dashboard_recipe_delete,
         name='dashboard_recipe_delete'),

    path('dashboard/recipe/<int:id>/edit/', 
         views.dashboard_recipe_edit,
         name='dashboard_recipe_edit'),
    
    
    path('dashboard/recipe/new/create/', 
         views.recipe_create_view,name='recipe_create'),

    path('profile/<int:id>/', 
         views.ProfileView.as_view(), name='profile'),


    
]

