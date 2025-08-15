from django.urls import path
from .details.template import views as template_views
from .details.overview import views as overview_views
from .details.other import views as other_views

urlpatterns = [
    path('template', template_views.ConfigurationTemplateViews.as_view(), name='config-template'),
    path('template/update', template_views.ConfigurationTemplateUpdate.as_view(), name='config-template'),
    path('stock/update', overview_views.ConfigurationOverviewUpdate.as_view(), name='config-stock-overview'),
    path('stock/delete', overview_views.ConfigurationOverviewDelete.as_view(), name='config-stock-overview'),
    path('balance', overview_views.ConfigurationOverviewBalance.as_view(), name='config-stock-overview'),
    path('stock', overview_views.ConfigurationOverviewViews.as_view(), name='config-stock-overview'),
    path('stock-detail', other_views.ConfigurationStockDetailViews.as_view(),
         name='config-template-stock'),
    path('all-stock-detail', other_views.ConfigurationAllStockDetailViews.as_view(),
         name='config-template-stock'),        
    path('stock/request-stoptrade', overview_views.ConfigurationOverviewRequestViews.as_view(), name='config-stock-overview-stoptrade-request'),
    path('stock/request-buy', overview_views.ConfigurationOverviewRequestViews.as_view(), name='config-stock-overview-buy-request'),
    path('stock/request-sell', overview_views.ConfigurationOverviewRequestViews.as_view(), name='config-stock-overview-sell-request')
]
