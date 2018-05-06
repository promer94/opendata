from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.core.validators import validate_email


def forbidden_username_validator(value):
    forbidden_usernames = ['admin', 'settings', 'news', 'about', 'help',
                           'signin', 'signup', 'signout', 'terms', 'privacy',
                           'cookie', 'new', 'login', 'logout', 'administrator',
                           'join', 'account', 'username', 'root', 'blog',
                           'user', 'users', 'billing', 'subscribe', 'reviews',
                           'review', 'blog', 'blogs', 'edit', 'mail', 'email',
                           'home', 'job', 'jobs', 'contribute', 'newsletter',
                           'shop', 'profile', 'register', 'auth',
                           'authentication', 'campaign', 'config', 'delete',
                           'remove', 'forum', 'forums', 'download',
                           'downloads', 'contact', 'blogs', 'feed', 'feeds',
                           'faq', 'intranet', 'log', 'registration', 'search',
                           'explore', 'rss', 'support', 'status', 'static',
                           'media', 'setting', 'css', 'js', 'follow',
                           'activity', 'questions', 'articles', 'network', ]

    if value.lower() in forbidden_usernames:
        raise ValidationError(_('This is a reserved word.'), code='name_forbid')


def invalid_username_validator(value):
    if '@' in value or '+' in value or '-' in value:
        raise ValidationError(_('Enter a valid username.'),  code='name_invalid',)


def unique_email_validator(value):
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError(_('User with this Email already exists.'), code='email_exists')


def unique_username_ignore_case_validator(value):
    if User.objects.filter(username__iexact=value).exists():
        raise ValidationError(_('User with this Username already exists.'), code='name_exists')


class SignUpForm(forms.ModelForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        required=True,
        validators=[forbidden_username_validator, invalid_username_validator, unique_username_ignore_case_validator]
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm your password",
        required=True)
    email = forms.CharField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        required=True,
        max_length=75,
        validators=[unique_email_validator, validate_email])

    class Meta:
        model = User
        exclude = ['last_login', 'date_joined']
        fields = ['username', 'email', 'password', 'confirm_password', ]

    def clean(self):
        super(SignUpForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and password != confirm_password:
            message = 'Passwords don\'t match'
            self.add_error('password', message)
        return self.cleaned_data

