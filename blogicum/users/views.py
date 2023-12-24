from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404

from blog.views import get_queryset
from .forms import CustomUserEditForm, User


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
    paginator = Paginator(get_queryset().filter(author_id=user.id), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context: dict = {
        'profile': user,
        'page_obj': page_obj
    }
    return render(request, 'blog/profile.html', context)


def edit(request, username):
    """View функция для страницы редактирования профиля"""
    instance = get_object_or_404(User, username=username)
    form = CustomUserEditForm(request.POST or None, instance=instance)
    context = {'form': form}
    if form.is_valid():
        form.save()
    return render(request, 'blog/user.html', context)
