from django.urls import path
from .views import LoginView, RegisterView, LogoutView, audit_log_view, profile_view

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("audit-log/", audit_log_view, name="audit_log"),
    path("profile/", profile_view, name="profile"),
]