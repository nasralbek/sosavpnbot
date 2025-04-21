from modules.databases.postgres.pg_base import Pg_base 

class Pg_keys_queries:
    table_name = "Users"
    INIT_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS %s (
user_id bigint NOT NULL,
bonuses int default 0,
invited_by bigint default NULL,
refferals int default 0,
key_uuid TEXT NOT NULL,
reg_time timestamp DEFAULT current_timestamp
)
"""  % table_name

    CREATE_USER_QUERY = """
INSERT INTO %s (user_id,bonuses,invited_by,refferals,key_uuid)
VALUES (%s,%s,%s,%s,%s)
""" % table_name



class Pg_key():
    def __init__(self,user_id,bonuses,invited_by,refferals):
        pass

class Pg_Keys(Pg_base):
    def __init__(self,*args,**kwargs):
        super().__init__()
        self.table_name = Pg_keys_queries.table_name
        self.create_if_not_exists(*args,**kwargs)

    def create_if_not_exists(self):
        query = Pg_keys_queries.INIT_TABLE_QUERY
        self.sync_query(query)

    async def create_user(self, key:Pg_key):
        query = Pg_keys_queries.CREATE_USER_QUERY
        await self.async_query(query,
                               key.user_id,
                               key.bonuses,
                               key.invited_by,
                               key.refferals,
                               key.key_uuid,
                               key.regtime)
