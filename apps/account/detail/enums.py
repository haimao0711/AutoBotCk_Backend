from enum import Enum

class AccountStatusEnum(Enum):
    Passive = 'Passive'
    Active = 'Active'
    
class AccountLoginStatusEnum(Enum):
    LoginSuccess = 'LoginSuccess'
    LoginFailed = 'LoginFailed'
    Logout = 'Logout'
    NotActive = 'NotActive'
    