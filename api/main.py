
from contextlib import asynccontextmanager
from fastapi import FastAPI
from remnawave_api import RemnawaveSDK

from config import Config
import database
from database.database import DataBase
import routers



import uvicorn

from services.admin.service import AdminService
import asyncio

async def on_startup(app: FastAPI):
    config = Config.load_from_env()
    
    app.state.r_sdk = RemnawaveSDK(base_url=config.remna.BASE_URL,
                        token = config.remna.TOKEN)
    
    app.state.db = DataBase(config.database)
    await app.state.db.initialize()

    app.state.admin_service = AdminService(config.adminbot,app.state.db,app.state.r_sdk)
    await app.state.admin_service.init_topics()
    await app.state.admin_service.notify_api_started()
    #app.state.admin_service.start_bot()



    routers.include_routers(app,
                            app.state.r_sdk,
                            app.state.db,
                            app.state.admin_service)


async def on_shutdown(app: FastAPI):

    await app.state.db.close()
    await app.state.admin_service.notify_api_stopped()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await on_startup(app)
    yield
    await on_shutdown(app)

    
def create_app() -> FastAPI:
    app = FastAPI(lifespan = lifespan)
    
    return app

app = create_app()

#if __name__ == "__main__":
#    uvicorn.run("main:app",host = "localhost",port = 8080,log_level = "debug",reload= True)
