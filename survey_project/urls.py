from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import include, path, reverse


def home_redirect(request):
    return HttpResponseRedirect(reverse("survey_app:home"))


urlpatterns = [
    path("admin/", admin.site.urls),
    path("survey/", include("survey_app.urls")),
    path("", home_redirect),
]
