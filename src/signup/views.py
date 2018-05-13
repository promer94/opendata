import os
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from app.fatsecret import Fatsecret
from .forms import SignUpForm
from .models import Profile
from datetime import datetime


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if not form.is_valid():
            return render(request, 'signup/register.html', {'form': SignUpForm(), 'errors': form.errors})
        else:
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            current_weight = form.cleaned_data.get('current_weight')
            current_height = form.cleaned_data.get('current_height')
            goal_weight = form.cleaned_data.get('goal_weight')
            new_user = User.objects.create_user(username=username, password=password, email=email)
            Profile.objects.create_profile(new_user, current_weight, current_height, goal_weight)
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/home')
    else:
        return render(request, 'signup/register.html', {'form': SignUpForm()})


def home(request):
    if request.user.is_authenticated():
        current_profile = Profile.objects.get(user=request.user)
        current_weight = current_profile.get_current_weight()
        goal_weight = current_profile.get_goal_weight()
        fs = Fatsecret(os.environ.get('API_KEY'), os.environ.get('API_SECRET'), current_profile.get_session_token())
        fs.exercise_entries_commit_day()
        food_record = fs.food_entries_get_month()
        food_record_data = []
        food_item_label = []
        food_calories = 0
        if food_record is not None:
            for item in food_record:
                food_record_data.append(int(item['calories']))
                food_calories = food_calories + int(item['calories'])
                food_item_label.append(int(item['date_int'])*24*60*60*1000)

        activities_record = fs.exercise_entries_get_month()
        activities_calories = 0
        activities_record_data = []
        activities_item_label = []
        if activities_record is not None:
            for item in activities_record:
                activities_record_data.append(int(item['calories']))
                if fs.unix_time(datetime.now()) == int(item['date_int']):
                    activities_calories = int(item['calories'])
                activities_item_label.append(int(item['date_int'])*24*60*60*1000)

        context = {'food_calories': food_calories,
                   'activities_calories': activities_calories,
                   'current_weight': current_weight,
                   'goal_weight': goal_weight,
                   'username': request.user.get_username(),
                   'food_record_data': food_record_data,
                   'food_item_label': food_item_label,
                   'activities_record_data': activities_record_data,
                   'activities_item_label': activities_item_label
                   }
        return render(request, 'home.html', context)
    else:
        return redirect('/')
