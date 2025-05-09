from math import ceil
from configs.main_config import day_price

class Converter:
    def days2price(days):
        price = ceil(days*day_price)
        return price

    def days2seconds():
        pass
    
    def days2mseconds():
        pass

    def mseconds2days():
        pass
    
    def seconds2days():
        pass
