from os import getenv


class os_attr_not_defined(Exception):
     def __init__(self, message):            
        super().__init__(message)

def get_os_attr(attrname="", default = None):
    result =  getenv(attrname,default)
    return result