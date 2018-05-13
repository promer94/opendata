"""fitsecret URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from app.views import search, entry_create, food_diary, activity, activities_add, activities_get
from django.contrib import admin


urlpatterns = [
    url(r'^', include('signup.urls')),
    url(r'^search', search, name='search'),
    url(r'^food/', food_diary, name='food_diary'),
    url(r'^food_entry/add', entry_create, name='food_entry_create'),
    url(r'^activities/', activity, name='activity'),
    url(r'^activity/add', activities_add, name='activities_add'),
    url(r'^activity/get', activities_get, name='activities_get'),
    url(r'^admin/', admin.site.urls),
]
