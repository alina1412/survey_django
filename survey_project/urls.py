
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, reverse
from survey_project import settings
from django.http import HttpResponseRedirect


def home_redirect(request):
    return HttpResponseRedirect(reverse('survey_app:home'))


urlpatterns = [
    path('admin/', admin.site.urls),
    path('survey_app/', include('survey_app.urls')),
    path('', home_redirect),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
