from django.urls import path, re_path

from movies import views

urlpatterns = [



    path('show/',views.show),
    path('search/<str:name>',views.search),
    path('about/<str:url>',views.about),
    re_path('^play/$', views.play),


]
