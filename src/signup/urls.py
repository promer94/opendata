from django.conf.urls import url, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'auth'
urlpatterns = [
    url(r'^home/', views.home, name='home'),
    url(r'^logout', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^register/', views.register, name='register'),
    url(r'^$', auth_views.LoginView.as_view(template_name='signup/cover.html', redirect_field_name='home'),
        name="login")
]
