from common.errors.messages import ErrorMessages
from .models import Candle

class CandleService:
    
    @staticmethod
    def check_exist_candle(candle_type):
        try:
            _ = Candle.objects.get(candle=candle_type)
            return True
        except (Candle.DoesNotExist):
            return False
        
    @staticmethod
    def get_candle(candle_type):
        try:
            candle = Candle.objects.get(candle=candle_type)
            return candle
        except (Candle.DoesNotExist):
            raise ValueError(ErrorMessages.CANDLE_DOES_NOT_EXIST)
    @staticmethod
    def get_candle_sell(candle_sell_type):
        try:
            candle_sell = Candle.objects.get(candle_sell=candle_sell_type)
            return candle_sell
        except (Candle.DoesNotExist):
            raise ValueError(ErrorMessages.CANDLE_DOES_NOT_EXIST)
            
