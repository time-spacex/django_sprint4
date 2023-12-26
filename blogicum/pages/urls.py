from django.urls import path

from . import views


app_name = 'pages'
handler403 = 'pages.views.csrf_failure'


urlpatterns: list = [
    path('about/', views.AboutPage.as_view(), name='about'),
    path('rules/', views.RulesPage.as_view(), name='rules'),
]
