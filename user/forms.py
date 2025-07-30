from django import forms
from captcha.fields import CaptchaField

from user.models import CustomUser, Profile


class UserForm(forms.ModelForm):
    captcha=CaptchaField()
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'last_name',
            'phone',
            'password',
            'captcha',
        ]

    def save(self, commit=True,*args, **kwargs):
        return CustomUser.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            last_name=self.cleaned_data['last_name'],
            password=self.cleaned_data['password'],
        )


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)



class ForgetPasswordForm(forms.Form):
    username = forms.CharField()



class ChangePasswordForm(forms.Form):
    code=forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    re_password = forms.CharField(widget=forms.PasswordInput)



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'nickname',
            'bio',
            'image'
        ]