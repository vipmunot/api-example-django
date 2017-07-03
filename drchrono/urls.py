from django.conf.urls import include, url, patterns
from django.views.generic import TemplateView
from django.contrib import  admin
import views
import settings

admin.autodiscover();

urlpatterns = [

    url(r'^$', views.get_access,name = "cId"),
    url(r'^home/$' , views.get_home, name='home'),
    url(r'^home/wishpatient/(?P<id>\d+)/$', views.wishpatient,name = "wishPatient"),
    url(r'^home/sendemail',views.sendEmail),
    url(r'^admin/',include(admin.site.urls)),

]
