from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()


class CustomUserEditForm(UserCreationForm):


    class Meta(UserCreationForm.Meta):

        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )


    def __init__(self, *args, **kwargs):
       super(UserCreationForm, self).__init__(*args, **kwargs)
       del self.fields['password1']
       del self.fields['password2']