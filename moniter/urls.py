from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index', views.index, name='index'),
    url(r'^$', views.login, name='login'),
    url(r'^reg_user', views.reg_user, name='reg_user'),
    url(r'^welcome', views.welcome),
    url(r'^first_welcome', views.welcome_first, name='first_welcome'),
    url(r'^edit_selectbase', views.edit_selectbase, name='edit_selectbase'),
    url(r'^order', views.order),
    url(r'^cate', views.cate),
    url(r'^member', views.member, name='member'),
    url(r'^del_data/(?P<spider_id>[0-9]+)$', views.del_data, name='del_data'),
    url(r'^status_edit/(.*?)$', views.edit_status, name='status_edit'),
    url(r'^edit/(?P<spider_id>[0-9]+)$', views.edit, name='edit'),
    url(r'^edit_action/', views.edit_action, name='edit_action'),
    url(r'^active_member', views.member_first, name='active_member'),
    url(r'^json_data', views.json_data, name='json_data'),
]