import string
import random

def generate_sub_id(length = 20):
    char_set = string.ascii_lowercase + string.ascii_uppercase + string.digits 
    return ''.join(random.choice(char_set) for _ in range(length))
