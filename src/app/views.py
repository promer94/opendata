import os
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .fatsecret import Fatsecret

# Create your views here.


@login_required(login_url='/')
def search(request):
    food = request.GET.get('food', 'apple')
    page = int(request.GET.get('page', 1))
    fs = Fatsecret(os.environ.get('API_KEY'),
                   os.environ.get('API_SECRET'))
    result, max_results, page_number, total_result = fs.foods_search(food, page_number=page-1, max_results=48)
    total_result = int(total_result)
    total_page = int(int(total_result)/int(max_results))+1
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




