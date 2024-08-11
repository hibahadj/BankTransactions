from django.shortcuts import redirect

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated for certain paths
        if not request.session.get('is_authenticated') and request.path not in ['/login/', '/logout/']:
            return redirect('login')
        response = self.get_response(request)
        return response