from django.urls import path
from .views import article_list, article_detail, create_article, add_category, add_subcategory, load_subcategories

urlpatterns = [
    path('', article_list, name='article_list'),
    path('article/<slug:slug>/', article_detail, name='article_detail'),
    path('create/', create_article, name='create_article'),
    path('category/add/', add_category, name='add-category'),
    path('subcategory/add/', add_subcategory, name='add-subcategory'),
    path('ajax/load-subcategories/', load_subcategories, name='ajax_load_subcategories'),
]
