import pytest
import modules.databases.gino.PG_API as PG_API

class TestGinoApi:
    def test_DB_API_INIT_success(self):
        API = PG_API()