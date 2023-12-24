from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()


class CustomUserEditForm(UserCreationForm):


    password1 = None
    password2 = None


    class Meta(UserCreationForm.Meta):

        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )
