from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from django.utils import timezone
from blog.models import Post, Category


def filter_published_posts(queryset):
    """Фильтрует публикации, проверяя статус публикации и дату."""
    current_time = timezone.now()    # Вынес переменную тоже отдельно,
    # показалось так будет правильно, или лучше вызов по месту как Вы написали?
    return queryset.filter(
        Q(is_published=True)
        & Q(pub_date__lte=current_time)
        & Q(category__is_published=True)
    )


def index(request):
    """Главная страница"""
    template_name = 'blog/index.html'

    post_list = filter_published_posts(
        Post.objects.select_related('author', 'category')
    ).order_by('-pub_date')[:5]

    context = {
        'post_list': post_list,
    }
    return render(request, template_name, context)


def category_posts(request, category_slug):
    """Фильтруем посты по категории"""
    category = get_object_or_404(Category, slug=category_slug,
                                 is_published=True)

    post_list = filter_published_posts(
        category.posts.select_related('author', 'category')
    ).order_by('-pub_date')

    context = {
        'category': category,
        'post_list': post_list,
    }
    return render(request, 'blog/category.html', context)


def post_detail(request, post_id):
    """Получаем публикацию, проверяя все условия или возвращаем 404"""
    post = get_object_or_404(
        filter_published_posts(
            Post.objects.select_related('author', 'category')
        ),
        id=post_id
    )

    context = {
        'post': post,
    }
    return render(request, 'blog/detail.html', context)
