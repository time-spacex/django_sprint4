from django.views.generic import TemplateView
from django.shortcuts import render


class AboutPage(TemplateView):
    """Класс для отображения страницы о проекте."""

    template_name = 'pages/about.html'


class RulesPage(TemplateView):
    """Класс для отображения списка правил."""

    template_name = 'pages/rules.html'


def page_not_found(request, exception):
    """View функция для кастомной страницы ошибки 404."""
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason=''):
    """View функция для кастомной страницы ошибки 403."""
    return render(request, 'pages/403csrf.html', status=403)


def server_error(request, exception=None):
    """View функция для кастомной страницы ошибки 500."""
    return render(request, 'pages/500.html', status=500)
