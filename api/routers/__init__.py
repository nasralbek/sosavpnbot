from fastapi import APIRouter, Depends, FastAPI
import remnawave_api
from database.database import DataBase
import routers.users
import routers.transactions
from remnawave_api import RemnawaveSDK

from services.admin.service import AdminService

def include_routers(app: FastAPI,
                    r_sdk: RemnawaveSDK, 
                    db : DataBase,
                    admin_service: AdminService):

    

    users = routers.users.Users(r_sdk,db,admin_service)
    transactions = routers.transactions.Transactions(db,admin_service)




    app.include_router(users.router)
    app.include_router(transactions.router)
