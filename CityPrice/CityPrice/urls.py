"""CityPrice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from web import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),

    path('map/', views.map),

    path('park/', views.park),
    path('park/add', views.parkAdd),
    path('park/add-from-file',views.parkAddFromFile),
    path('park/edit/<int:nid>', views.parkEdit),
    path('park/delete/<int:nid>', views.parkDelete),

    path('district/', views.district),
    path('district/add', views.districtAdd),
    path('district/edit/<int:nid>', views.districtEdit),
    path('district/delete/<int:nid>', views.districtDelete),

    path('house/', views.house),

    path('school/', views.school),
    path('school/add', views.schoolAdd),
    path('school/edit/<int:nid>', views.schoolEdit),
    path('school/delete/<int:nid>', views.schoolDelete),

    path('hospital/', views.hospital),
    path('hospital/add', views.hospitalAdd),
    path('hospital/edit/<int:nid>', views.hospitalEdit),
    path('hospital/delete/<int:nid>', views.hospitalDelete),

    path('test/', views.pageTest),

]
