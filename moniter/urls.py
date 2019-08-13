from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index', views.index, name='index'),
    url(r'^$', views.login, name='login'),
    url(r'^reg_user', views.reg_user, name='reg_user'),
    url(r'^welcome', views.welcome),
    url(r'^first_welcome', views.welcome_first, name='first_welcome'),
    url(r'^order$', views.order),
    url(r'^cate', views.cate),
    url(r'^member', views.member, name='member'),
    url(r'^del_data/(?P<spider_id>[0-9]+)$', views.del_data, name='del_data'),
    url(r'^status_edit/(.*?)$', views.edit_status, name='status_edit'),
    url(r'^edit/(?P<spider_id>[0-9]+)$', views.edit, name='edit'),
    url(r'^edit_action/', views.edit_action, name='edit_action'),
    url(r'^active_member', views.member_first, name='active_member'),
    url(r'^json_data', views.json_data, name='json_data'),
    url(r'^editimport/(?P<spider_id>[0-9]+)$', views.order_view, name='editimport'),
    url(r'^del_order_view/(?P<spider_id>[0-9]+)$', views.del_order_view, name='del_order_view'),
    url(r'^edit_order_view', views.edit_order_view, name='edit_order_view'),
    url(r'^show_result', views.show_result, name='show_result'),
    url(r'^table_data', views.table_data, name='table_data'),
]