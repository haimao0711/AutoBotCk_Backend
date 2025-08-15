from django.urls import path
from .views import TradingViews, TradingViewsIsTrading
from .scheduler_api import start_scheduler_user_api, stop_scheduler_user_api, get_scheduler_status_user_api
urlpatterns = [
  path('vps', TradingViews.as_view(), name='trading-views'),
    path('is_trading', TradingViewsIsTrading.as_view(), name='trading-views'),
    path('scheduler/user/start/', start_scheduler_user_api, name='start_scheduler_user'),
    path('scheduler/user/stop/', stop_scheduler_user_api, name='stop_scheduler_user'),
    path('scheduler/user/status/<int:user_id>/', get_scheduler_status_user_api, name='get_scheduler_status_user'),
]
