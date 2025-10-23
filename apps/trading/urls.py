from django.urls import path
from .views import (
    TradingViews, 
    TradingViewsIsTrading, 
    StartSchedulerAPIView, 
    StopSchedulerAPIView, 
    SchedulerStatusAPIView
)

urlpatterns = [
    path('vps', TradingViews.as_view(), name='trading-views'),
    path('is_trading', TradingViewsIsTrading.as_view(), name='trading-views'),
    path('scheduler/start/', StartSchedulerAPIView.as_view(), name='start_scheduler'),
    path('scheduler/stop/', StopSchedulerAPIView.as_view(), name='stop_scheduler'),
    path('scheduler/status/', SchedulerStatusAPIView.as_view(), name='scheduler_status'),
]
