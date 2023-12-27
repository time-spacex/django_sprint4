from django.urls import include, path

from . import views


urlpatterns: list = [
    path('auth/', include('django.contrib.auth.urls')),
    path(
        'auth/registration/',
        views.UserCreateView.as_view(),
        name='registration'
    ),
    path('profile/<str:username>/', views.profile_overview, name='profile'),
    path(
        'profile/<str:username>/edit/',
        views.profile_edit,
        name='edit_profile'
    ),
]
