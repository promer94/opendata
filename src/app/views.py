import os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .fatsecret import Fatsecret

# Create your views here.


@login_required(login_url='/')
def search(request):
    food = request.GET.get('food', 'apple')
    page = request.GET.get('page', 0)
    fs = Fatsecret(os.environ.get('API_KEY', '303b21a907694b1ea8d5cbdc0d817774'),
                   os.environ.get('API_SECRET', '0aefd2d9ba604cbfa5c0a79a910cb419'))
    result, max_results, page_number, total_result = fs.foods_search(food)
    context = {'result_list': result}
    return render(request, 'app/search.html', context)




