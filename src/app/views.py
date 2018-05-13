import os
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .fatsecret import Fatsecret
from signup.models import Profile
from .models import FoodEntry
from datetime import date, datetime
# Create your views here.


@login_required(login_url='/')
def search(request):
    food = request.GET.get('food', 'apple')
    page = int(request.GET.get('page', 1))
    fs = Fatsecret(os.environ.get('API_KEY'),
                   os.environ.get('API_SECRET'))

    # Pagination
    result, max_results, page_number, total_result = fs.foods_search(food, page_number=page - 1, max_results=6)
    total_result = int(total_result)
    total_page = int(int(total_result) / int(max_results)) + 1

    # Get serving_id
    for item in result:
        if isinstance(fs.food_get(item['food_id'])['servings']['serving'], dict):
            item['serving_methods'] = [fs.food_get(item['food_id'])['servings']['serving']]
        elif isinstance(fs.food_get(item['food_id'])['servings']['serving'], list):
            item['serving_methods'] = fs.food_get(item['food_id'])['servings']['serving']
        else:
            pass

    if page == 1:
        context = {'food': food,
                   'result_list': result,
                   'page': page,
                   'total_page': total_page,
                   'next_page': page + 1
                   }
    elif page == total_page:
        context = {'food': food,
                   'result_list': result,
                   'page': page,
                   'total_page': total_page,
                   'previous_page': page - 1
                   }
    elif page > total_page or page < 1:
        raise HttpResponseBadRequest
    else:
        context = {'food': food,
                   'result_list': result,
                   'page': page,
                   'total_page': total_page,
                   'previous_page': page - 1,
                   'next_page': page + 1
                   }
    return render(request, 'app/search.html', context)


@login_required(login_url='/')
def entry_create(request):
    if request.method == 'POST':
        current_user = request.user
        current_profile = Profile.objects.get(user=current_user)

        session_token = current_profile.get_session_token()
        fs = Fatsecret(os.environ.get('API_KEY'), os.environ.get('API_SECRET'), session_token=session_token)

        current_date = date.today().strftime("%Y%m%d")
        food_id = request.POST.get('food')
        meal = request.POST.get('meal')
        serving_id = request.POST.get('servingId')
        unit_number = request.POST.get('unit')
        food_name = request.POST.get('foodName')
        if unit_number == '':
            return JsonResponse({'error': 1})
        else:
            unit_number = float(request.POST.get('unit'))
            food_serve_name = food_name
            food_entry_id = fs.food_entry_create(food_id, food_serve_name,
                                                 serving_id,
                                                 unit_number,
                                                 meal
                                                 )['value']
            FoodEntry.objects.create(profile=current_profile, food_entry_id=food_entry_id)
            return JsonResponse({'success': 1})
    else:
        raise HttpResponseBadRequest


@login_required(login_url='/')
def food_diary(request):
    current_profile = Profile.objects.get(user=request.user)
    fs = Fatsecret(os.environ.get('API_KEY'), os.environ.get('API_SECRET'), current_profile.get_session_token())
    id_collection = list(current_profile.foodentry_set.all())
    food_record = fs.food_entries_get_month()
    food_calories = 0
    if food_record is not None:
        for item in food_record:
            food_calories = food_calories + int(item['calories'])
    breakfast = []
    lunch = []
    dinner = []
    other = []
    for food_ids in id_collection:
        food = fs.food_entries_get(food_ids.__str__())[0]

        date_int = int(food['date_int'])
        date_string = datetime.utcfromtimestamp(date_int*24*60*60).strftime('%Y%m%d')
        food['date_int'] = date_string

        if food['meal'] == 'Breakfast':
            breakfast.append(food)
        elif food['meal'] == 'Lunch':
            lunch.append(food)
        elif food['meal'] == 'Dinner':
            dinner.append(food)
        elif food['meal'] == 'Other':
            other.append(food)

    food_record = fs.food_entries_get_month()
    pie_chart_data = {}
    if food_record is not None:
        food_record = food_record[-1]
        pie_chart_data['Fat'] = float(food_record['fat'])
        pie_chart_data['Protein'] = float(food_record['protein'])
        pie_chart_data['Carbohydrate'] = float(food_record['carbohydrate'])

    context = {'breakfast': breakfast,
               'lunch': lunch,
               'dinner': dinner,
               'other': other,
               'food_calories': food_calories,
               'pie_chart_data': pie_chart_data
               }
    return render(request, 'app/foodDiary.html', context)


@login_required(login_url='/')
def activity(request):
    current_profile = Profile.objects.get(user=request.user)
    fs = Fatsecret(os.environ.get('API_KEY'), os.environ.get('API_SECRET'), current_profile.get_session_token())
    record = fs.exercise_entries_get()
    activities_record = fs.exercise_entries_get_month()
    activities_calories = 0
    if activities_record is not None:
        for item in activities_record:
            if fs.unix_time(datetime.now()) == int(item['date_int']):
                activities_calories = int(item['calories'])
    context = {'record': record, 'activities_calories': activities_calories}
    return render(request, 'app/activityRecord.html', context)


@login_required(login_url='/')
def activities_add(request):
    current_profile = Profile.objects.get(user=request.user)
    fs = Fatsecret(os.environ.get('API_KEY'), os.environ.get('API_SECRET'), current_profile.get_session_token())
    new_activity = request.GET.get('newType')
    time = int(request.GET.get('time'))
    old_activity = request.GET.get('oldType')
    fs.exercise_entry_edit(shift_to_id=new_activity, shift_from_id=old_activity, minutes=time)
    fs.exercise_entries_commit_day()
    record = fs.exercise_entries_get()
    name = []
    data = []
    for item in record:
        name.append(item['exercise_name'])
        data.append(int(item['calories']))

    activities_record = fs.exercise_entries_get_month()
    activities_calories = 0
    if activities_record is not None:
        for item in activities_record:
            if fs.unix_time(datetime.now()) == int(item['date_int']):
                activities_calories = int(item['calories'])

    return JsonResponse({'label': name, 'data': data, 'activities_calories': activities_calories})


@login_required(login_url='/')
def activities_get(request):
    current_profile = Profile.objects.get(user=request.user)
    fs = Fatsecret(os.environ.get('API_KEY'), os.environ.get('API_SECRET'), current_profile.get_session_token())
    activities_record = fs.exercise_entries_get_month()
    activities_calories = 0
    if activities_record is not None:
        for item in activities_record:
            if fs.unix_time(datetime.now()) == int(item['date_int']):
                activities_calories = int(item['calories'])
    record = fs.exercise_entries_get()
    name = []
    data = []
    for item in record:
        name.append(item['exercise_name'])
        data.append(int(item['calories']))
    return JsonResponse({'label': name, 'data': data})


