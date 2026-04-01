from django.urls import path
from apps.account.detail.views import AccountViews, AccountTradingView, AccountDetailView, ResetBotView, put_admin
from .exchange import views as exchange_views

urlpatterns = [
    path('vps', AccountViews.as_view(), name='account-list-create'),
    path('vps/', AccountDetailView.as_view(), name='account-detail-get'),
    path('vps-subaccount', AccountDetailView.as_view(),
         name='account-detail-subaccount'),
    path('status-trade', AccountTradingView.as_view(),
         name='account-trading-subaccount'),
    path('block-trade', AccountTradingView.as_view(),
         name='account-trading-subaccount'),
    path('reset_bot', ResetBotView.as_view(),
         name='reset-bot'),
    path('vps/admin', put_admin, name='admin-update-account'),
    path('exchange', exchange_views.ExchangeViews.as_view(), name='exchange'),
]
