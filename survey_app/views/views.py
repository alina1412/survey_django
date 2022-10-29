import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from survey_app.crud import delete_demo_user, get_or_create_demo_user
from survey_app.models import User
from survey_app.views.utils import get_menu, menu, menu_notlog

logger = logging.getLogger(__name__)


def login_user(request, user):
    login(request, user)
    messages.success(request, "logged in")


def home_view(request):
    menu_copy = get_menu(request)
    if not request.user.is_authenticated and request.method == "POST":
        user = get_or_create_demo_user()
        login_user(request, user)
        return redirect("survey_app:survey_list")
    return render(
        request,
        "home.html",
        {
            "menu": menu_copy,
            "h3": "To make and answer surveys is easy",
            "auth": request.user.is_authenticated,
        },
    )


def logout_view(request):
    delete_demo_user(request)
    logout(request)
    messages.success(request, "logged out")
    return HttpResponseRedirect(reverse("survey_app:home"))


class RegisterView(CreateView):
    template_name = "register.html"
    form_class = UserCreationForm
    model = User
    extra_context = {
        "title": "register",
        "h3": "Register for creating surveys",
        "menu": menu_notlog + menu,
    }

    def get_success_url(self):
        messages.success(self.request, "registered")
        return reverse_lazy("survey_app:login")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class SurveyLoginView(LoginView):
    template_name = "login.html"
    form_class = AuthenticationForm
    extra_context = {"title": "login", "h3": "Login", "menu": menu_notlog + menu}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def get_success_url(self):
        return reverse_lazy("survey_app:survey_list")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        raw_password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=raw_password)
        login_user(self.request, user)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "wrong username or password")
        return self.render_to_response(self.get_context_data(form=form))
