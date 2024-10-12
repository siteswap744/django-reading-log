from django.contrib.auth.views import LoginView
from django.urls import reverse


class MyLoginView(LoginView):
    def get_success_url(self):
        return reverse("reading_log:individual_log", args=[self.request.user.id])
