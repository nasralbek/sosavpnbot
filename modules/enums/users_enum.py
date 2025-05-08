from enum import Enum


class RegisterUserEnum(Enum):
    register_success = 0
    register_failed = 1
    user_already_exists = 3
