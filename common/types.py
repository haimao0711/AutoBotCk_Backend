from .success.types import SuccessType
from .errors.types import ErrorType

class CommonTypeSerivce:
    def check_response_type(res_type):
        if res_type in [SuccessType.CREATE_SUCCESS, SuccessType.UPDATED_SUCCESS]:
            return True
        elif res_type in [ErrorType.CREATE_FAILED, ErrorType.UPDATE_FAILED]:
            return False
        return True
