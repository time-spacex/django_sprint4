from django.shortcuts import render


def about(request):
    """View функция для отображения страницы о проекте."""
    return render(request, 'pages/about.html')


def rules(request):
    """View функция для отображения списка правил."""
    return render(request, 'pages/rules.html')
