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
    
    @staticmethod
    def get_candle_second(candle_second_type):
        # Chuẩn hóa giá trị 'Off' hoặc 'None' thành 'OFF' (key trong enum)
        if candle_second_type in ['Off', 'None', 'NONE']:
            candle_second_type = 'OFF'
        try:
            candle_second = Candle.objects.get(candle=candle_second_type)
            return candle_second
        except (Candle.DoesNotExist):
            # Nếu không tìm thấy, tạo mới Candle object với 'OFF'
            if candle_second_type == 'OFF':
                candle_second = Candle.objects.create(
                    name='OFF',
                    candle='OFF',
                    candle_second='OFF',
                    candle_sell='OFF',
                    candle_sell_second='OFF'
                )
                return candle_second
            raise ValueError(ErrorMessages.CANDLE_DOES_NOT_EXIST)
    
    @staticmethod
    def get_candle_sell_second(candle_sell_second_type):
        # Chuẩn hóa giá trị 'Off' hoặc 'None' thành 'OFF' (key trong enum)
        if candle_sell_second_type in ['Off', 'None', 'NONE']:
            candle_sell_second_type = 'OFF'
        # Tìm Candle object có candle_sell=candle_sell_second_type (giống như get_candle_sell)
        # vì các Candle objects được tạo với trường candle_sell, không phải candle_sell_second
        try:
            candle_sell_second = Candle.objects.get(candle_sell=candle_sell_second_type)
            return candle_sell_second
        except (Candle.DoesNotExist):
            # Nếu không tìm thấy theo candle_sell, thử tìm theo candle
            try:
                candle_sell_second = Candle.objects.get(candle=candle_sell_second_type)
                return candle_sell_second
            except (Candle.DoesNotExist):
                # Nếu không tìm thấy, tạo mới Candle object với 'OFF'
                if candle_sell_second_type == 'OFF':
                    candle_sell_second = Candle.objects.create(
                        name='OFF',
                        candle='OFF',
                        candle_second='OFF',
                        candle_sell='OFF',
                        candle_sell_second='OFF'
                    )
                    return candle_sell_second
                raise ValueError(ErrorMessages.CANDLE_DOES_NOT_EXIST)
            
