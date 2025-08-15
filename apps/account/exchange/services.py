from common.errors.messages import ErrorMessages
from .models import Exchange

class ExchangeService:
    def check_exchange_exist(exchange_code):
        try:
            _ = Exchange.objects.get(exchange_code=exchange_code)
            return True
        except Exchange.DoesNotExist:
            return False
        
    def get_exchange_by_id(exchange_id):
        try:
            exchange = Exchange.objects.get(id=exchange_id)
            return exchange
        except Exchange.DoesNotExist:
            raise ValueError(ErrorMessages.EXCHANGE_DOES_NOT_EXIST)

    def get_exchange_by_code(exchange_code):
        try:
            exchange = Exchange.objects.get(code=exchange_code)
            return exchange
        except Exchange.DoesNotExist:
            raise ValueError(ErrorMessages.EXCHANGE_DOES_NOT_EXIST)
        
    def get_exchanges():
        exchange = Exchange.objects.all()
        return exchange
    
    
