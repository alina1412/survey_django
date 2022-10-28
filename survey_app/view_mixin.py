from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin


class LoginRequiredMixin(AccessMixin):
    login_url = "survey_app:login"
    permission_denied_message = "Not logged"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(self.request, self.permission_denied_message)
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
