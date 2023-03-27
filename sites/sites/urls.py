"""sites URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from users.views import index, about_startup,base_template,card_template,about_template,startups_template
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add_startup=<str:tg_user_id>', index, name='add_startup'),
    path('about_startup=<str:startup_id>', about_startup, name='about_startup'),
    path('', base_template, name='base_template'),
    path('startups/', startups_template, name='startups_template'),
    path('about', about_template, name='about_template'),
    path('card=<str:tg_user_id>/',card_template,name='card_template')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
