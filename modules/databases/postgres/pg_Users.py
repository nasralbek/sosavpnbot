from modules.databases.postgres.pg_base import Pg_base
from modules.databases.postgres.Pg_enums import RegisterUserStatus
from uuid import uuid4
class Pg_users_queries:
    table_name = "Users"

    INIT_TABLE_QUERY = """

CREATE TABLE IF NOT EXISTS %s (
user_id bigint NOT NULL,
bonuses int default 0,
invited_by bigint default NULL,
refferals int default 0,
key_uuid TEXT NOT NULL,
regtime timestamp DEFAULT current_timestamp
)

"""  % table_name
    
    CREATE_USER_QUERY = """

INSERT INTO %s (user_id,bonuses,invited_by,refferals,key_uuid)
VALUES (%s,%s,%s,%s,%s)

    """.replace("%s",table_name,1)

    SELECT_USER_WHERE_USER_ID = """

SELECT * FROM %s 
WHERE user_id = %s

""".replace("%s",table_name,1)



class Pg_user():
    def __init__(self,user_id,bonuses,invited_by,refferals,regtime=None,key_uuid=None):
        self.user_id    = user_id
        self.bonuses    = bonuses
        self.invited_by = invited_by
        self.refferals  = refferals
        self.regtime    = regtime
        if key_uuid is None:
            self.key_uuid   = uuid4()
        else:self.key_uuid = key_uuid

    def from_execute_result(execute_reuslt : list):
        user_id     = execute_reuslt[0]
        bonuses     = execute_reuslt[1]
        invited_by  = execute_reuslt[2]
        refferals   = execute_reuslt[3]
        key_uuid    = execute_reuslt[4]
        regtime     = execute_reuslt[5]
        return Pg_user(user_id,
                       bonuses,
                       invited_by,
                       refferals,
                       key_uuid=key_uuid,
                       regtime=regtime)
    def __str__(self):
        return """Pg_user object:\n
user_id:%s
bonuses:%s
invited_by:%s
referrals:%s
key_uuid:%s
regtime:%s
""" % (self.user_id ,  
self.bonuses,
self.invited_by,
self.refferals,
self.key_uuid,
self.regtime)

class Pg_Users(Pg_base):
    def __init__(self,*args,**kwargs):
        super().__init__()
        self.table_name = Pg_users_queries.table_name
        self.create_if_not_exists(*args,**kwargs)

    def create_if_not_exists(self):
        query = Pg_users_queries.INIT_TABLE_QUERY
        self.sync_query(query,())

    async def create_user(self, user:Pg_user) ->RegisterUserStatus:
        query = Pg_users_queries.CREATE_USER_QUERY
        result = await self.async_query(query,
                               (user.user_id,
                               user.bonuses,
                               user.invited_by,
                               user.refferals,
                               user.key_uuid,))
        return result
    async def get_user(self,user_id) -> Pg_user:
        query = Pg_users_queries.SELECT_USER_WHERE_USER_ID
        excute_result = await self.async_query(query,(user_id,))
        
