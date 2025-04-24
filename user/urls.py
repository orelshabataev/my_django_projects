from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.messages.api import success
from django.urls import path, reverse_lazy

from user.views import LoginUser, registor_user, ProfileView, UserPasswordChangeView

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('password_change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(template_name='user/password_change_done.html'), name='password_change_done'),

    path('password-reset/', PasswordResetView.as_view(template_name='user/password_reset_form.html'), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), name='password_reset_done'),

    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html',
                                                                                    success_url=reverse_lazy('password_reset_complete')), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), name='password_reset_complete'),

    path('registor/', registor_user, name='registor'),
    path('profile/', ProfileView.as_view(), name='profile')
]