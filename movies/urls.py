from django.urls import path

from movies import views

urlpatterns = [



    path('show/',views.show),
    path('search/',views.search),
    path('about/<str:url>',views.about),
    path('play/<str:url>/',views.play)

]
