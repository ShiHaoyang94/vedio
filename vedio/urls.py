"""Note_Cloud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls import path, include

import index.views
from index import views as index_views
from vedio import view, settings
from movies import views
from user import views as user_views
urlpatterns = [


    path('admin/', admin.site.urls),
    path('user/',include('user.urls')),
    path('index/',include('index.urls')),
    path('',view.login),
    path('busy/',user_views.busy),
    path('movies/',include('movies.urls')),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)