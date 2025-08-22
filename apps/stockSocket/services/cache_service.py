# apps/stockSocket/services/cache_service.py
from django.core.cache import cache

PRICE_CACHE_KEY = "stock_prices"  # key duy nhất để lưu tất cả giá

def update_price(symbol: str, price: float):
    """
    Cập nhật giá realtime vào Redis
    """
    prices = cache.get(PRICE_CACHE_KEY, {})
    prices[symbol] = price
    cache.set(PRICE_CACHE_KEY, prices, timeout=None)

def get_price(symbol: str) -> float:
    """
    Lấy giá hiện tại từ Redis
    """
    prices = cache.get(PRICE_CACHE_KEY, {})
    return prices.get(symbol, 0.0)
