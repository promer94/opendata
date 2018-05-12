import os
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .fatsecret import Fatsecret
from signup.models import Profile
from .models import FoodEntry
from datetime import date


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
        if unit_number == '':
            return JsonResponse({'error': 1})
        else:
            unit_number = float(request.POST.get('unit'))
            food_serve_name = current_date + ',' + current_user.get_username() + ',' + meal
            food_entry_id = fs.food_entry_create(food_id,
                                                 food_serve_name,
                                                 serving_id,
                                                 unit_number,
                                                 meal
                                                 )['value']
            FoodEntry.objects.create(profile=current_profile, food_entry_id=food_entry_id)
            return JsonResponse({'success': 1})
    else:
        raise HttpResponseBadRequest
