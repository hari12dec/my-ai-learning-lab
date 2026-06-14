from django.conf.urls import url
from fakenewsApp import views
from django.urls import path

app_name = 'fakenewsApp'

urlpatterns = [
    path('', views.fakedataView.as_view(), name = 'fake'),
    #path('train/extract', viewss.extractFace.as_view(), name = 'face'),
    #path('train/embed', viewss.Faceembedd.as_view(), name = 'embed'),
    #path('train/svcmodel', viewss.getsvc.as_view(), name = 'svc'),

    #path('result', views.resultcheck1.as_view(), name = 'result'),
    #path('success', views.Success.as_view(), name = 'success'),
    #path('fail',views.Failure.as_view(),name='fail'),
    #path('filenot',views.FileNotfound.as_view(), name='filenot'),
    #path('aboutus',views.AboutUs.as_view(), name='aboutus')
]
