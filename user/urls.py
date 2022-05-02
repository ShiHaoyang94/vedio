from django.urls import path
from . import views
urlpatterns = [

    path('login/',views.login),
    path('register/',views.register),
    path('check/',views.check),
    path('exit/',views.exit),
    path('check/resend/',views.re),
    path('forget/',views.forget),
    path('forget/check/',views.f_check),
    path('forget/check/resend/',views.res),
    path('forget/new/',views.new),
    path('qunfa/', views.qunfa),
]