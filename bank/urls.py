from django.conf.urls import url

from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^account', views.AccountView.as_view(), name='account'),
    url(r'^acc_list', views.acc),
    url(r'^acc_info/(?P<accNum>\w+)/$', views.acc_info),
    url(r'^deposit/$', views.deposit, name='deposit'),
    #url('', views.index, name='index'),
    url('^transfer/$', views.transfer, name='transfer'),
	]

urlpatterns = format_suffix_patterns(urlpatterns)
