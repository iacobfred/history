from django.urls import include, path, re_path

from apps.users import views

app_name = 'users'

urlpatterns = [
    path(
        'password_change/', views.PasswordChangeView.as_view(), name='password_change'
    ),
    path(
        'password_change/done/',
        views.PasswordChangeView.as_view(),
        name='password_change_done',
    ),
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path(
        'password_reset/done/',
        views.PasswordResetView.as_view(),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        views.PasswordResetView.as_view(),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete',
    ),
    re_path(r'profile/?', views.ProfileView.as_view(), name='profile'),
    path('', include('django.contrib.auth.urls')),
]
