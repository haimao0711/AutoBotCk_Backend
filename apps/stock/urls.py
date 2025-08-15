from django.urls import path

from . import views as stock_views


urlpatterns = [
    path('', stock_views.StockViews.as_view(), name='stock'),
    path('trigger-download', stock_views.StockImportedViews.as_view(), name='download-stock')
]
