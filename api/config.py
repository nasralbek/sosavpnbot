from pydantic import BaseModel


class DatabaseConfig(BaseModel):
    HOST    : str | None
    PORT    : int | None
    NAME    : str
    USERNAME: str | None
    PASSWORD: str | None

    def url(self, driver: str = "postgresql+asyncpg") -> str:
        # if driver.startswith("sqlite"):
        #     return f"{driver}:////{DEFAULT_DATA_DIR}/{self.NAME}.{DB_FORMAT}"
        return f"{driver}://{self.USERNAME}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"

    @classmethod
    def load_from_env(cls) -> "DatabaseConfig":
        env = Env()
        env.read_env()
        return cls(
            HOST        = env.str("POSTGRES_HOST"),
            PORT        = env.int("POSTGRES_PORT"),
            NAME        = env.str("POSTGRES_DB"),
            USERNAME    = env.str("POSTGRES_USER"),
            PASSWORD    = env.str("POSTGRES_PASSWORD")
        )
 
class RemnawaveConfig(BaseModel):
    BASE_URL : str
    TOKEN: str

    @classmethod 
    def load_from_env(cls) -> "RemnawaveConfig":
        env = Env()
        env.read_env()
        return cls(
            BASE_URL    = env.str("REMNAWAVE_BASE_URL"),
            TOKEN       = env.str("REMNAWAVE_TOKEN")
        )
        
class AdminBotConfig(BaseModel):
    API_TOKEN: str
    ADMIN_CHAT_ID: str
    ADMINS: list[int] = []

    @classmethod
    def load_from_env(cls) -> "AdminBotConfig":
        env = Env()
        env.read_env()
        return cls(
            API_TOKEN = env.str("ADMIN_BOT_TOKEN"),
            ADMIN_CHAT_ID = env.str("ADMIN_CHAT_ID"),
            ADMINS = [int(admin) for admin in env.list("BOT_ADMINS", [])]
        )

class Config(BaseModel):
    remna: RemnawaveConfig
    database: DatabaseConfig
    adminbot: AdminBotConfig

    @classmethod
    def load_from_env(cls) -> "Config":
        return cls(
            remna    = RemnawaveConfig.load_from_env(),
            database = DatabaseConfig.load_from_env(),
            adminbot = AdminBotConfig.load_from_env()
        )

