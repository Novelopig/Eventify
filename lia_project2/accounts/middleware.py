from django.shortcuts import redirect
from django.conf import settings


class BlockNonAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            request.path.startswith("/admin/")
            and request.user.is_authenticated
            and not request.user.is_staff
        ):
            return redirect("homepage")

        return self.get_response(request)
