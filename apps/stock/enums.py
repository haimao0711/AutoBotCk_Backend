from enum import Enum

class SecondTimeEnums(Enum):
    SECOND_IN_WEEK= 604800
    SECOND_IN_DAY = 86400
    SECOND_IN_HOUR = 3600        
    SECOND_IN_QUARTER_HOUR = 900
    SECOND_IN_FIVE_MINUTES = 300   
    SECOND_IN_MINUTES = 60
    SECOND_IN_MINUTE = 60
        
        
class DataParamsTimeEnums(Enum):
    W1 = '1W'
    D1 = '1D'
    H1 = '60'
    M15 = '15'
    M5 = '5'
    M1 = '1'


class DownloadStatusEnum(Enum):
    NEW = 0
    EXIST = 1
    
class DownloadCoefficientNewEnum(Enum):
    W1 = 1000
    D1 = 200
    H1 = 56
    M15 = 24
    M5 = 10
    M1 = 3
    
class DownloadCoefficientMondayNewEnum(Enum):
    W1 = 1000
    D1 = 200
    H1 = 56
    M15 = 24
    M5 = 10
    M1 = 3
    
class DownloadCoefficientWeekendNewEnum(Enum):
    W1 = 1000
    D1 = 200
    H1 = 56
    M15 = 24
    M5 = 4
    M1 = 3
    
class DownloadCoefficientExistEnum(Enum):
    W1 = 1000
    D1 = 3
    H1 = 3
    M15 = 3
    M5 = 3
    M1 = 3
    
class DownloadCoefficientMondayExistEnum(Enum):
    W1 = 3
    D1 = 3
    H1 = 3
    M15 = 3
    M5 = 5
    M1 = 5
    
class DownloadCoefficientWeekendExistEnum(Enum):
    W1 = 3
    D1 = 3
    H1 = 3
    M15 = 3
    M5 = 5
    M1 = 5
    
    

class DayOfWeekEnum(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6
