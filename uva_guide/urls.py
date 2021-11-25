from django.urls import path
from . import views
from django.conf.urls import url


app_name = 'uva_guide'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # path('<int:year>/<str:month>/', views.cale, name='cale'),
    path('calendar', views.CalendarView.as_view(), name='cal'),
    path('event/new', views.event, name='event_new'),
    path('event/edit/<event_id>', views.event, name='event_edit'),
    path('login_user', views.login_user, name='login-user'),
    path('profile_setup', views.get_profile_setup, name='profile-setup')
]
