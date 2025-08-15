from enum import Enum

class LoginStatusEnum(Enum):
    BY_PASS_PASSWORD = 'True Password'
    BY_PASS_OTP = 'True OTP'
    FAILED_PASSWORD = 'Wrong Password'
    FAILED_OTP = 'Wrong OTP'
