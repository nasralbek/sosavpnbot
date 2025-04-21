from enum import Enum

class RegisterUserStatus(Enum):
    register_succes = 0
    register_failed = 1
    already_exists = 2
    
