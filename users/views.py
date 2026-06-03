import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.views.generic import View

from .forms import LoginForm, RegisterForm
from .models import AuditLog

logger = logging.getLogger(__name__)


class LoginView(View):
    """
    Login view
    get(): Returns the login page with the login form
    post(): Authenticates the user and logs them in
    """

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, "users/login.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        ip = request.META.get("REMOTE_ADDR")

        if form.is_valid():
            email    = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user     = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                AuditLog.objects.create(
                    user=user,
                    action="LOGIN_SUCCESS",
                    description=f"User {user.email} logged in successfully.",
                    ip_address=ip,
                )
                logger.info(f"User {user.email} logged in")
                return redirect(request.GET.get("next", "home"))

            # Failed login
            AuditLog.objects.create(
                user=None,
                action="LOGIN_FAILED",
                description=f"Failed login attempt for email: {email}",
                ip_address=ip,
            )
            logger.warning(f"Invalid login attempt for {email}")
            form.add_error(None, "Invalid email or password")

        return render(request, "users/login.html", {"form": form})


class RegisterView(View):
    """
    Register view
    get(): Returns the register page with the register form
    post(): Registers the user
    """

    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        return render(request, "users/register.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password")
            user.set_password(password)
            user.save()

            user_group = Group.objects.get(name="User")
            user.groups.add(user_group)

            login(request, user)
            logger.info(f"User {user.email} registered and added to User group")
            return redirect("login")

        logger.warning(f"Invalid registration attempt: {form.errors}")
        return render(request, "users/register.html", {"form": form})


class LogoutView(View):
    """
    Logout view
    get(): Logs the user out
    """

    def get(self, request, *args, **kwargs):
        AuditLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            action="LOGOUT",
            description=f"User {request.user} logged out.",
            ip_address=request.META.get("REMOTE_ADDR"),
        )
        logout(request)
        logger.info("User logged out")
        return redirect("login")


@login_required
def audit_log_view(request):
    if not request.user.groups.filter(name="Admin").exists():
        AuditLog.objects.create(
            user=request.user,
            action="ACCESS_DENIED",
            description="Unauthorized attempt to access audit log page.",
            ip_address=request.META.get("REMOTE_ADDR"),
        )
        return HttpResponseForbidden("Access Denied: Admins only.")

    logs = AuditLog.objects.select_related("user").all()[:500]
    return render(request, "users/audit_log.html", {"logs": logs})

@login_required
def profile_view(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.save()
        AuditLog.objects.create(
            user=user,
            action='UPDATE',
            description=f'User {user.email} updated their profile.',
            ip_address=request.META.get('REMOTE_ADDR'),
        )
        return redirect('profile')
    return render(request, 'users/profile.html', {'user': request.user})