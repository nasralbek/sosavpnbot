import modules.databases.postgres.pg_Users as Pg_users 
from modules.databases.postgres.Pg_enums import RegisterUserStatus

class Pg_db_api():
    def __init__(self):
        self.useres =  Pg_users()
        self.keys = Pg_keys()

        
    def register_user(self,user:Pg_users.Pg_user) -> RegisterUserStatus:
        self.users.create_user(user)
