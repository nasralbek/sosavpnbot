import psycopg2
import os
from configs.main_config import PG_CONFIG


def get_os_attr(attrname=""):
    return os.environ.get(attrname)


class Pg_base():
    def __init__(self,dbname = PG_CONFIG.PG_DB_NAME,
                 user = PG_CONFIG.PG_USERNAME,
                 password=PG_CONFIG.PG_PASSWORD,
                 host=PG_CONFIG.PG_HOST,
                 port=PG_CONFIG.PG_PORT):
        self.dbname = dbname
        self.user=user
        self.password = password
        self.host = host
        self.port = port
        self.connection = psycopg2.connect(dbname = self.dbname
                                           ,user=self.user
                                           ,password=self.password,
                                           host=self.host,
                                           port=self.port)

    def from_env():
        return Pg_base(
            get_os_attr("PG_DATABASE"),
            get_os_attr("PG_USER"),
            get_os_attr("PG_PASSWORD"),
            get_os_attr("PG_HOST"),
            get_os_attr("PG_PORT"))
    
    async def async_query(self,query: str,*args,**kwargs):
        async with self.connection.cursor() as cursor:
            result = await cursor.execute(query,*args,**kwargs)
            return result

    def sync_query(self,query:str,*args):
        with self.connection.cursor() as cursor:
            result = cursor.execute(query,args)
            self.connection.commit()
            return result