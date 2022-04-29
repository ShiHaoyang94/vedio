from django.urls import path

from movies import views

urlpatterns = [



    path('show/',views.show),
    path('search/<int:page>/',views.search),
    path('about/<str:url>/<str:urls>/',views.about),
    path('play/<str:url>/',views.play)

]
