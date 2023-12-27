from datetime import datetime

from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .models import Post, Category, Comment
from .forms import PostForm, CommentForm


def get_queryset(show_post_for_author=False, show_comment_count=True):
    """Функция для получения базового QuerySet."""
    queryset = Post.objects.select_related(
        'author',
        'location',
        'category'
    )
    if not show_post_for_author:
        return_queryset = queryset.filter(
            pub_date__lt=datetime.today(),
            is_published=True,
            category__is_published=True
        )
    else:
        return_queryset = queryset
    if show_comment_count:
        return_queryset_annotated = return_queryset.annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')
    else:
        return_queryset_annotated = return_queryset
    return return_queryset_annotated


def get_page_number(queryset, request):
    """Функция, создающая постраничный вывод постов."""
    paginator = Paginator(queryset, settings.POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def index(request):
    """View функция для формирования и отображения постов в виде списка."""
    page_obj = get_page_number(get_queryset(), request)
    context: dict = {'page_obj': page_obj}
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    """Функция для отображения страницы детализации поста."""
    post = get_object_or_404(
        get_queryset(True, False), pk=post_id
    )
    if post.author != request.user and (
        post.is_published is False
        or post.pub_date.replace(tzinfo=None) > datetime.today()
        or post.category.is_published is False
    ):
        raise Http404
    comments = post.comments.filter(is_published=True)
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
    page_obj = get_page_number(
        get_queryset().filter(
            category=category
        ), request
    )
    context: dict = {
        'page_obj': page_obj,
        'category': category
    }
    return render(request, 'blog/category.html', context)


@login_required
def post_create(request):
    """View функция создания формы нового поста."""
    form = PostForm(
        request.POST or None,
        files=request.FILES or None
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
    if instance.author != request.user:
        return redirect('blog:post_detail', post_id=post_id)
    form = PostForm(request.POST or None, instance=instance)
    context = {'form': form}
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/create.html', context)


@login_required
def post_delete(request, post_id):
    """View функция удаления отдельного поста."""
    instance = get_object_or_404(get_queryset(), pk=post_id)
    if instance.author != request.user:
        return redirect('blog:post_detail', post_id=post_id)
    form = PostForm(request.POST or None, instance=instance)
    context = {'form': form}
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:index')
    return render(request, 'blog/create.html', context)


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
    instance = get_object_or_404(
        Comment.objects.filter(
            post_id=post_id
        ), pk=comment_id
    )
    form = CommentForm(request.POST or None, instance=instance)
    context = {'comment': instance, 'form': form}
    if form.is_valid() and instance.author == request.user:
        form.save()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/comment.html', context)


@login_required
def coment_delete(request, post_id, comment_id):
    """View функция для удаления комментариев к публикации."""
    instance = get_object_or_404(
        Comment.objects.filter(
            post_id=post_id
        ), pk=comment_id
    )
    if request.method == 'POST' and instance.author == request.user:
        instance.delete()
        return redirect('blog:post_detail', post_id=post_id)
    context = {'comment': instance}
    return render(request, 'blog/comment.html', context)
