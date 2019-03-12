"""testfk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from sign import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/$', views.index),
    url(r'^login_action/$', views.login_action),
    url(r'^read_plan/$', views.read_plan),
    url(r'^accounts/login/$', views.index),
    url(r'^search_name/$',views.search_name),
    url(r'^guest_manage/$',views.guest_manage),
    url(r'^search_guest/$',views.search_guest),
    url(r'^add_index/$',views.add_index),
    url(r'^add_index_action/$',views.add_index_action),
    #与之前略有不同，括号内的内容匹配读书列表id，限制只能是数字，匹配的数字rid将会作为update_index()视图函数的参数
    url(r'^update_index/(?P<rid>[0-9]+)/$', views.update_index),
    #url(r'^update_index/$', views.update_index),
    url(r'^update_index_action/(?P<rid>[0-9]+)/$', views.update_index_action), #编辑提交
    url(r'^logout/$',views.logout),
]
