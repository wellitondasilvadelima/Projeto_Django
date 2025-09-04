from django.shortcuts import render,get_list_or_404,get_object_or_404
from recipes.models import Recipe
from django.http import Http404 
from django.db.models import Q
from django.http import JsonResponse
from utils.pagination import make_pagination
import os
from django.utils import translation
from django.utils.translation import gettext as _

PER_PAGE = int(os.environ.get('PER_PAGE',6))

def home(request):
     recipes = Recipe.objects.filter(is_published=True).select_related(
          'author', 'category').prefetch_related('author__profile').order_by('-id')
     
     page_obj, pagination_range = make_pagination(request,recipes,PER_PAGE)
     html_language = translation.get_language()

     return render(request, 'recipes/pages/home.html',context={
          'recipes' : page_obj,
          'pagination_range': pagination_range,
          'html_language': html_language,
     })

def homeAPI(request):
     recipes = Recipe.objects.filter(is_published=True).select_related(
          'author', 'category').order_by('-id').values(
                              "id",
                              "title",
                              "description",
                              "slug",
                              "preparation_time",
                              "preparation_time_unit",
                              "servings",
                              "servings_unit",
                              "preparation_steps",
                              "created_at",
                              "updated_at",
                              "is_published",
                              "cover",
                              "category__name",
                              "author__username"
                         )

     return JsonResponse (
          list(recipes),
          safe=False
     )

def recipedetailAPI(request,id):
     recipe = Recipe.objects.filter(pk=id,is_published=True).select_related(
     'author', 'category').values(
                              "title",
                              "description",
                              "slug",
                              "preparation_time",
                              "preparation_time_unit",
                              "servings",
                              "servings_unit",
                              "preparation_steps",
                              "created_at",
                              "updated_at",
                              "is_published",
                              "cover",
                              "category__name",
                              "author__username"
                              ).first()
     if recipe:
          recipe["cover"] = request.build_absolute_uri(recipe["cover"])
     return JsonResponse (
          recipe,
          safe=False
     )

def category(request,category_id):
     recipes = get_list_or_404(Recipe.objects.filter(
          category__id=category_id,is_published=True).order_by('-id'))
     
     page_obj, pagination_range = make_pagination(request,recipes,PER_PAGE)
     category_tranlate = _('Category')
     return render(request, 'recipes/pages/category.html',context={
          'recipes' : page_obj,
          'title' : f'{recipes[0].category.name} {category_tranlate} |',
          'pagination_range':pagination_range,
     })

def recipe(request,id):
     recipe = get_object_or_404(Recipe, pk=id,is_published=True)
      
     return render(request, 'recipes/pages/recipe-view.html',context={
          'recipe' : recipe,
          'is_datail_page' : True,
     })

def search(request):
    term = request.GET.get('q','').strip()

    if not term :
         raise Http404() 
    
    recipes = Recipe.objects.filter(
          Q(
               Q(title__icontains=term) |
               Q(description__icontains=term)
          ), is_published = True,    
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(request,recipes,PER_PAGE)
    search_tranlate = _('Search for')
    return render(request, 'recipes/pages/search.html', {
         'page_title': f'{search_tranlate} "{term}" |"',
         'search_term': term,
         'recipes': page_obj,
         'pagination_range' : pagination_range,
         'additional_url_query': f'&q={term}'
    })