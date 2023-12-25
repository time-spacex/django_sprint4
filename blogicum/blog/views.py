from datetime import datetime

from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import Post, Category, Comment
from .forms import PostForm, CommentForm


def get_queryset():
    """Функция для получения базового QuerySet."""
    return Post.objects.select_related(
        'author',
        'location',
        'category'
    ).filter(
        pub_date__lt=datetime.today(),
        is_published=True,
        category__is_published=True
    )


def index(request):
    """View функция для формирования и отображения постов в виде списка."""
    paginator = Paginator(get_queryset(), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context: dict = {'page_obj': page_obj}
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    """Функция для отображения страницы детализации поста."""
    post = get_object_or_404(
        get_queryset(),
        pk=post_id
    )
    comments = Comment.objects.select_related(
        'author',
        'post'
    ).filter(post__id=post_id)
    context: dict = {
        'post': post, 
        'comments': comments,
        'form': CommentForm()
    }
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    """View функция для отображения постов по категориям."""
    category = get_object_or_404(
        Category,
        is_published=True,
        slug=category_slug
    )
    paginator = Paginator(
        get_queryset().filter(
        category__slug=category_slug
        ), 10
    )
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context: dict = {
        'page_obj': page_obj,
        'category': category
    }
    return render(request, 'blog/category.html', context)


@login_required
def post_create(request, post_id=None):
    """View функция создания формы нового поста."""
    if post_id is not None:
        instance = get_object_or_404(Post, pk=post_id)
    else:
        instance = None
    form = PostForm(request.POST or None,
                    instance=instance,
                    files=request.FILES or None,
        )
    context = {'form': form}
    if form.is_valid():
        form.save(commit=False)
        form.instance.author = request.user
        form.save()
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/create.html', context)


@login_required
def post_edit(request, post_id):
    """View функция редактирования отдельного поста."""
    instance = get_object_or_404(get_queryset(), pk=post_id)
    if instance.author == request.user:
        form = PostForm(request.POST or None, instance=instance)
        context = {'form': form}
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id=post_id)
        return render(request, 'blog/create.html', context)
    else:
        return redirect('blog:post_detail', post_id=post_id)


@login_required
def post_delete(request, post_id):
    """View функция удаления отдельного поста."""
    instance = get_object_or_404(get_queryset(), pk=post_id)
    if instance.author == request.user:
        form = PostForm(request.POST or None, instance=instance)
        context = {'form': form}
        if request.method == 'POST':
            instance.delete()
            return redirect('blog:index')
        return render(request, 'blog/create.html', context)
    else:
        return redirect('blog:post_detail', post_id=post_id)


@login_required
def coment_create(request, post_id):
    """View функция для сохранения комментариев к публикации."""
    post = get_object_or_404(get_queryset(), pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', post_id=post_id)


@login_required
def coment_edit(request, post_id, comment_id):
    """View функция для редактирования комментариев к публикации."""
    instance = get_object_or_404(Comment.objects.filter(
        post_id=post_id
        ), pk=comment_id
    )
    form = CommentForm(request.POST or None, instance=instance)
    context = {'comment': instance, 'form': form}
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/comment.html', context)


@login_required
def coment_delete(request, post_id, comment_id):
    """View функция для удаления комментариев к публикации."""
    instance = get_object_or_404(Comment.objects.filter(
        post_id=post_id
        ), pk=comment_id
    )
    context = {'comment': instance}
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/comment.html', context)
