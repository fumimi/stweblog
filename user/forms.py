from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm

from .models import User


class RegisterForm(forms.ModelForm):
    """ユーザー登録画面用のフォーム"""

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'ユーザー名'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'パスワード'}),
        }

    password2 = forms.CharField(
        label='確認用パスワード',
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': '確認用パスワード'}),
    )


    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['email'].widget.attrs = {'placeholder': 'メールアドレス'}
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"



    def clean_username(self):
        value = self.cleaned_data['username']
        if len(value) < 2:
            raise forms.ValidationError(
                '%(min_length)s文字以上で入力してください', params={'min_length': 2})
        return value

    def clean_email(self):
        value = self.cleaned_data['email']
        if len(value) < 2:
            raise forms.ValidationError(
                '%(min_length)s文字以上で入力してください', params={'min_length': 2})
        return value

    def clean_password(self):
        value = self.cleaned_data['password']
        return value

    def clean(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError("パスワードと確認用パスワードが合致しません")
        super(RegisterForm, self).clean()


class LoginForm(forms.Form):
    """ログイン画面用のフォーム"""

    username = UsernameField(
        label='ユーザー名',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'ユーザー名', 'autofocus': True}),
    )

    password = forms.CharField(
        label='パスワード',
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'パスワード'}, render_value=True),
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user_cache = None
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


    def clean_password(self):
        value = self.cleaned_data['password']
        return value

    def clean_username(self):
        value = self.cleaned_data['username']
        if len(value) < 2:
            raise forms.ValidationError(
                '%(min_length)s文字以上で入力してください', params={'min_length': 2})
        return value

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        try:
            user = get_user_model().objects.get(username=username)
        except ObjectDoesNotExist:
            raise forms.ValidationError("正しいユーザー名を入力してください")
        if not user.check_password(password):
            raise forms.ValidationError("正しいユーザー名とパスワードを入力してください")
        self.user_cache = user

    def get_user(self):
        return self.user_cache


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email',)

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {'placeholder': 'ユーザー名'}
        self.fields['email'].required = True
        self.fields['email'].widget.attrs = {'placeholder': 'メールアドレス'}
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def clean_username(self):
        value = self.cleaned_data['username']
        if len(value) < 2:
            raise forms.ValidationError(
                '%(min_length)s文字以上で入力してください', params={'min_length': 2})
        return value

    def clean_email(self):
        value = self.cleaned_data['email']
        return value
