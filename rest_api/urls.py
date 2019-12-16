
#from rest_framework import routers
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import Selected_Device 
from .views import All_Device, less_than_temp, between_time
from .views import  greater_than_temp, between_humidity

urlpatterns = {
    url(r'^Selected_Device/',Selected_Device.as_view(), name="Delete"),  
    url(r'^All_Device/',All_Device.as_view(), name="list"),
    url(r'^less_than_temp/',less_than_temp.as_view(), name="list1"),
    url(r'^greater_than_temp/',greater_than_temp.as_view(), name="list2"),    
    url(r'^between_humidity/',between_humidity.as_view(), name="list3"), 
    url(r'^between_time/',between_time.as_view(), name="list4"),  
    #url(r'^updatedTime/',updatedTime.as_view(), name="list4"),  
}
    
urlpatterns = format_suffix_patterns(urlpatterns)

















# urlpatterns = {
#    # url(r'^bucketlists/$', CreateView.as_view(), name="create"),
#     #url(r'^list/', ListAPIView.as_view(), name="create1"),
#     #url(r'^bucketlist/delete/(?P<pk>[0-9]+)/$', DeleteView.as_view(), name="delete"),
#    # url(r'^bucketlists/delete/(?P<pk>[0-9]+)/$',DeleteView.as_view(), name="Delete"),
#     url(r'^bucketlists/Selected_Device/',Selected_Device.as_view(), name="Delete"),  
#     url(r'^bucketlists/All_Device/',All_Device.as_view(), name="list"), 
#     #url(r'^bucketlists/Delete_All_Device/',Delete_All_Device.as_view(), name="list"), 
#    # url('bucketlists/', include('rest_framework.urls', namespace='rest_framework'))


# }