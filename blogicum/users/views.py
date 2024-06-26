from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404

from blog.views import get_queryset, get_page_number
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


def profile_overview(request, username):
    """View функция для обзорной страницы профиля с его постами."""
    user = get_object_or_404(User, username=username)
    page_obj = get_page_number(
        get_queryset(
            add_filters_to_queryset=(request.user != user),
            show_comment_count=True
        ).filter(author=user), request
    )
    context: dict = {
        'profile': user,
        'page_obj': page_obj
    }
    return render(request, 'blog/profile.html', context)


@login_required
def profile_edit(request):
    """View функция для страницы редактирования профиля."""
    form = CustomUserEditForm(request.POST or None, instance=request.user)
    context = {'form': form}
    if form.is_valid():
        form.save()
    return render(request, 'blog/user.html', context)
