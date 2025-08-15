"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # api
    path('api/user/', include('apps.authencation.urls')),
    path('api/stock', include('apps.stock.urls')),
    path('api/account/', include('apps.account.urls')),
    # path('api/account/', include('apps.balance.urls')),
    path('api/config/', include('apps.configuration.urls')),
    path('api/', include('apps.otp.urls')),
    path('api/transaction', include('apps.transaction.urls')),
    path('api/stock-exchange/', include('apps.authencation_exchange.urls')),
    path('api/trading/', include('apps.trading.urls'))
]
