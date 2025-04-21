import psycopg
import os
from configs.main_config import PG_CONFIG


def get_os_attr(attrname=""):
    return os.environ.get(attrname)


class Pg_base():
    def __init__(self,
                 dbname = PG_CONFIG.PG_DB_NAME,
                 user = PG_CONFIG.PG_USERNAME,
                 password = PG_CONFIG.PG_PASSWORD,
                 host = PG_CONFIG.PG_HOST,
                 port = PG_CONFIG.PG_PORT):
        
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection_kwargs = {  "dbname" : self.dbname,
                                    "user" : self.user,
                                    "password" : self.password,
                                    "host" : self.host,
                                    "port" : self.port}
        #self.connection = psycopg.connect(**self.connection_kwargs)

    def from_env():
        return Pg_base(
            get_os_attr("PG_DATABASE"),
            get_os_attr("PG_USER"),
            get_os_attr("PG_PASSWORD"),
            get_os_attr("PG_HOST"),
            get_os_attr("PG_PORT"))
    
    async def async_query(self,query: str,params):
        async with await psycopg.AsyncConnection.connect(**self.connection_kwargs) as aconnection:
            async with aconnection.cursor() as acursor:
                result = await acursor.execute(query,params=params)
                await aconnection.commit()        
                try:
                    res = await acursor.fetchall()
                except:
                    return []


    def sync_query(self,query:str,params):
        with  psycopg.Connection.connect(**self.connection_kwargs) as connection:
            with connection.cursor() as cursor:
                result = cursor.execute(query,params = params)
                connection.commit()
        return result