from django.conf.urls import url
from . import views           # Import views from current directory

urlpatterns = [
	url(r'^$', views.index),     # Linking to views.index #Remember commas!!
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^home$', views.home),
    url(r'^logout$', views.logout),
#add next two together for link to work
    url(r'^all_users$', views.all_users),
    url(r'^(?P<player_id>\d+)$', views.player, name='player'),
    url(r'^play_game$', views.play_game),
    url(r'^process$', views.process),
    # url(r'^clear$', views.clear),
] #Remember closing bracket!!
