from django.shortcuts import get_object_or_404, render
from blog.models import Post, Category
from django.db.models import Q
from django.utils import timezone


def index(request):
    """Главная страница"""
    template_name = 'blog/index.html'
    current_time = timezone.now()

    post_list = Post.objects.select_related('author', 'category').filter(
        Q(is_published=True) & Q(pub_date__lte=current_time)
        & Q(category__is_published=True)
    ).order_by('-pub_date')[:5]

    context = {
        'post_list': post_list,
    }
    return render(request, template_name, context)


def category_posts(request, category_slug):
    """Фильтруем посты по категории"""
    category = get_object_or_404(Category, slug=category_slug,
                                 is_published=True)

    current_time = timezone.now()

    post_list = Post.objects.select_related('author', 'category').filter(
        Q(category=category) & Q(is_published=True)
        & Q(pub_date__lte=current_time)
    ).order_by('-pub_date')

    context = {
        'category': category,
        'post_list': post_list,
    }
    return render(request, 'blog/category.html', context)


def post_detail(request, post_id):
    """Получаем публикацию, проверяя все условия или возвращаем 404 ошибку"""
    current_time = timezone.now()

    post = get_object_or_404(
        Post.objects.select_related('author', 'category'),
        Q(id=post_id) & Q(is_published=True)
        & Q(pub_date__lte=current_time)
        & Q(category__is_published=True)
    )

    context = {
        'post': post,
    }
    return render(request, 'blog/detail.html', context)
