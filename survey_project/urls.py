
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from survey_project import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('survey_app/', include('survey_app.urls'))
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
