from django.contrib.auth import logout
from django.utils import timezone
from .models import TokenBlacklist

class TokenExpiryCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated and if the token has expired
        if request.user.is_authenticated:
            token_entry = TokenBlacklist.objects.filter(user=request.user).first()
            if token_entry and token_entry.expires_at < timezone.now():
                token_entry.delete()
                # If the token has expired, log out the user
                logout(request)

        response = self.get_response(request)
        return response
    
    #  Remove all user 
    
    # def __call__(self, request):
    #     # Retrieve all token entries that have expired
    #     expired_tokens = TokenBlacklist.objects.filter(expires_at__lt=timezone.now())

    #     # Iterate over expired tokens
    #     for token_entry in expired_tokens:
    #         # Logout the user associated with the expired token
    #         logout(request)

    #         # Delete the token entry from the database
    #         token_entry.delete()

    #     response = self.get_response(request)
    #     return response

