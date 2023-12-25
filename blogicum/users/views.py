from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404

from blog.models import Post
from .forms import CustomUserEditForm


User = get_user_model()


class UserCreateView(CreateView):
    """
    CBV функция создает форму регистрации и авторизации пользователя,
    перенаправляет на главную страницу.
    """

    template_name = 'registration/registration_form.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('blog:index')


def profile(request, username):
    """View функция для обзорной страницы профиля с его постами."""
    user = get_object_or_404(User, username=username)
    paginator = Paginator(Post.objects.select_related(
        'author',
        'location',
        'category'
        ).filter(author_id=user.id), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context: dict = {
        'profile': user,
        'page_obj': page_obj
    }
    return render(request, 'blog/profile.html', context)


def edit(request, username):
    """View функция для страницы редактирования профиля."""
    instance = get_object_or_404(User, username=username)
    if instance.username == request.user.username:
        form = CustomUserEditForm(request.POST or None, instance=instance)
        context = {'form': form}
        if form.is_valid():
            form.save()
        return render(request, 'blog/user.html', context)
    else:
        raise Http404
