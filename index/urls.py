from django.urls import path

from index import views

urlpatterns = [



    path('',views.index),
    path('<str:name>',views.indexs),
    path('tiyu/<str:name>/',views.tiyu),
    path('douyin/jiexi/',views.douyin),
    path('elsfk/',views.elsfk),
    path('xbw/',views.xbw),
    path('words/',views.words),
    path('laji/',views.laji),
    path('main/',views.main),


]
