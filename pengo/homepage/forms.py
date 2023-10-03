    
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User

class UsernameChangeForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username']
        help_texts = {
            'username': None,
        }
