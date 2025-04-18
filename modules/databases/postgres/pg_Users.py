from modules.databases.postgres.pg_base import Pg_base 

class Pg_users_queries:
    table_name = "Users"
    INIT_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS %s (
user_id int

)


"""  % table_name


class Pg_Users(Pg_base):
    def __init__(self,*args,**kwargs):
        super().__init__()
        self.table_name = Pg_users_queries.table_name
        self.create_if_not_exists(*args,**kwargs)

    def create_if_not_exists(self):
        query = Pg_users_queries.INIT_TABLE_QUERY
        self.sync_query(query)
