import os

class os_attr_not_defined(Exception):
     def __init__(self, message):            
        super().__init__(message)

def get_os_attr(attrname=""):
    result =  os.environ.get(attrname)
    if not result:
        raise os_attr_not_defined(f"os variable : {attrname} not defined")
    return result