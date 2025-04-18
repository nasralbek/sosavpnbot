import pytest
import modules.databases.postgres.pg_base as pg_base
import modules.databases.postgres.pg_Users as pg_users

class TestPgBase:
    def test_os_read(self):
        import os
        test_var_excepted_value = "excepted123321"
        test_var_name = "test_var"
        os.environ[test_var_name] = test_var_excepted_value 
        assert pg_base.get_os_attr(test_var_name) == test_var_excepted_value 
        
    def test_os_read_none(self):
        assert pg_base.get_os_attr() == None

    def test_init_success(self):
        try:
            db_name = pg_base.get_os_attr("PG_DATABASE")
            db_user = pg_base.get_os_attr("PG_USER")
            db_password = pg_base.get_os_attr("PG_PASSWORD")
            db_host = pg_base.get_os_attr("PG_HOST")
            db_port = pg_base.get_os_attr("PG_PORT")
        except:
            raise "error while getting os attrs"
        pg_base.Pg_base(db_name,db_user,db_password,db_host,db_port)
    
    def test_from_env(self):
        pg_base.Pg_base.from_env()

   
class TestPgUsersClass:
    def test_init_succes(self):
        pg_users.Pg_Users()

    def test_users_instance(self):
        object = pg_users.Pg_Users()
        assert isinstance(object,pg_users.Pg_Users)

    def tests_users_not_equal_base(self):
        assert not (pg_users.Pg_Users() == pg_base.Pg_base.from_env())
        
