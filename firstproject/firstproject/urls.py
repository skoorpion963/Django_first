"""firstproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path , include


from polls import views 

from django.urls import re_path
from django.views.static import serve
from django.conf import settings


urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path('admin/', admin.site.urls),
    path('tablev1', views.tableV1 ,name="tablev1"),
    path('', views.home , name= 'home'),
    path('home', views.home , name= 'home'),
    path('api', views.api , name= 'api'),
    path('table', views.table , name= 'table'),
    path('api/v1/simbollist/',views.SimbolApiView.as_view() ),
    path('api/v1/<str:simbol>/<str:interval>/', views.CryptoTransactionView.as_view(), name='crypto_transaction_api'),
    path('api/v1/<str:table>/', views.TableViewView.as_view(), name='crypto_transaction_api'),

    
]



