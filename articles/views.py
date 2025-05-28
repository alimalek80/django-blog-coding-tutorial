from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Category, SubCategory, Comment
from .forms import ArticleForm, CommentForm, CategoryForm, SubCategoryForm

# Create your views here.
def articles(request):
    return None

def article_list(request):
    categories = Category.objects.all()
    articles = Article.objects.all()
    return render(request, 'articles/article_list.html', {'categories': categories, 'articles': articles})

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    comments = article.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
            return redirect('article_detail', slug=article.slug)
    else:
        form = CommentForm()

    return render(request, 'articles/article_detail.html', {'article': article, 'comments': comments, 'form': form})

def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('article_list')
    else:
        form = ArticleForm()
    category_form = CategoryForm()
    subcategory_form = SubCategoryForm()
    return render(request, 'articles/create_article.html', {
        'form': form,
        'category_form': category_form,
        'subcategory_form': subcategory_form
    })

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('create_article')


def add_subcategory(request):
    if request.method == 'POST':
        form = SubCategoryForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('create_article')

