from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import CustomUser

class EmailPhoneUsernameBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in with 
    username, email, or phone number
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None
        
        try:
            # Try to fetch the user by searching username, email, or phone
            user = CustomUser.objects.get(
                Q(username=username) | Q(email=username) | Q(phone_number=username)
            )
        except CustomUser.DoesNotExist:
            # Run the default password hasher once to reduce timing attacks
            CustomUser().set_password(password)
            return None
        except CustomUser.MultipleObjectsReturned:
            # This shouldn't happen due to unique constraints
            return None
        
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        return None