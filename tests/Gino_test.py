import pytest
import modules.database.database as database
from tools.users_enum import RegisterUserEnum 

from gino import Gino
import random 
class TestGinoApi:

    async def get_db_manager(self):
        self.PG_DB_NAME = "postgres"
        self.PG_USERNAME = "postgres"
        self.PG_PASSWORD = "changeme"
        self.PG_HOST = "127.0.0.1"
        self.PG_PORT = "5432"
        return await database.DatabaseManager.auth( self.PG_HOST,
                                                        self.PG_PORT,
                                                        self.PG_DB_NAME,
                                                        self.PG_USERNAME,
                                                        self.PG_PASSWORD)
        
    @pytest.mark.asyncio
    async def test_db_manager_init_success(self):
        db_manager = await self.get_db_manager()
        assert isinstance(db_manager,database.DatabaseManager)
        await db_manager.init_tables()


    @pytest.mark.asyncio
    async def test_register_user_wo_ref(self):
        db_manager = await self.get_db_manager()
        user_id = random.randint(1000,2000)
        user = await db_manager.register_user(user_id)
        assert user == RegisterUserEnum.register_success

    @pytest.mark.asyncio
    async def test_reg_user_with_ref(self):
        db_manager = await self.get_db_manager()
        user_id = random.randint(1000,2000)
        ref_id = random.randint(1000,2000)
        ref_status = await db_manager.register_user(ref_id)
        new_user_status = await db_manager.register_user(user_id,ref_id)
        
        assert ref_status == RegisterUserEnum.register_success
        assert new_user_status == RegisterUserEnum.register_success

    @pytest.mark.asyncio
    async def test_reg_user_already_exists(self):
        db_manager = await self.get_db_manager()
        user_id = random.randint(1000,2000)
        first_res = await db_manager.register_user(user_id)
        second_res = await db_manager.register_user(user_id)
        assert first_res == RegisterUserEnum.register_success
        assert second_res == RegisterUserEnum.user_already_exists
     
                                                       

