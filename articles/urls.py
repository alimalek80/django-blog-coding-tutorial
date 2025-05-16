from django.urls import path
from .views import article_list, article_detail, create_article

urlpatterns = [
    path('', article_list, name='article_list'),
    path('article/<slug:slug>/', article_detail, name='article_detail'),
    path('create/', create_article, name='create_article'),
]