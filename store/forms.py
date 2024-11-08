from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth import get_user_model

class ChangePasswordForm(SetPasswordForm):

    class Meta:
        model = get_user_model()
        fields = ['new_password1','new_password2']

class SignUpForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('email','password1','password2')

class UpdateUserForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields =  ["username",'email']
