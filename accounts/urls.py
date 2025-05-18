from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name="home"),
    path('signin/', views.signin_view, name='signin'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path("verify-email/<str:token>/", views.verify_email, name="verify_email"),
    path("resend-verification-email/", views.resend_verification_email, name="resend_verification_email"),
    path("change-password/", views.change_password, name="change_password"),

    # New Paths for Password Reset
    path("password-reset/", views.password_reset_request, name="password_reset_request"),
    path("password-reset-done/", views.password_reset_done, name="password_reset_done"),
    path("password-reset-confirm/<str:token>/", views.password_reset_confirm, name="password_reset_confirm"),
    path("password-reset-complete/", views.password_reset_complete, name="password_reset_complete"),
]
