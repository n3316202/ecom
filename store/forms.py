from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

class SignUpForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('email','password1','password2')

class UpdateUserForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields =  ["username",'email']
