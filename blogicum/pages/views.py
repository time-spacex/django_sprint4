from django.views.generic import TemplateView


class AboutPage(TemplateView):
    """Класс для отображения страницы о проекте."""

    template_name = 'pages/about.html'


class RulesPage(TemplateView):
    """Класс для отображения списка правил."""

    template_name = 'pages/rules.html'
