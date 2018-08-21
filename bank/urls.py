from django.conf.urls import url

from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^account_list/$', views.account_list, name='account_list'),
    url(r'^account_detail/(?P<accNum>\w+)/$', views.account_info, name='account_detail'),
    url(r'^deposit/$', views.deposit, name='deposit'),
    url('^transfer/$', views.transfer, name='transfer'),
	]

urlpatterns = format_suffix_patterns(urlpatterns)
