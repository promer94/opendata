from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from .forms import SignUpForm


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if not form.is_valid():
            return render(request, 'signup/register.html', {'form': SignUpForm(), 'errors': form.errors})
        else:
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, password=password,
                                     email=email)
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    else:
        return render(request, 'signup/register.html', {'form': SignUpForm()})


def home(request):
    if request.user.is_authenticated():
        context = {'username': request.user.get_username()}
        return render(request, 'home.html', context)
    else:
        return redirect('/login')


