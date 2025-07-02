from dotenv import load_dotenv
from environs import Env
from dataclasses import dataclass
from pathlib import Path

import logging
from logging.handlers import MemoryHandler

DEFAULT_BOT_HOST = "0.0.0.0"
DEFAULT_BOT_PORT = 2000

DEFAULT_LOG_FORMAT = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DATA_DIR    = BASE_DIR / "data"
DEFAULT_LOCALES_DIR = BASE_DIR / "locales"
DEFAULT_PLANS_DIR   = DEFAULT_DATA_DIR / "plans.json"


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
memory_handler = MemoryHandler(capacity=100, flushLevel=logging.ERROR)
memory_handler.setFormatter(logging.Formatter(DEFAULT_LOG_FORMAT))
logger.addHandler(memory_handler)

@dataclass
class BotConfig:
    TOKEN       : str
    BOT_VPN_NAME: str
    ADMINS      : list[int]
    DEV_ID      : int
    SUPPORT_ID  : int
    DOMAIN      : str
    PORT        : int
    CHANNEL_TAG : str
    CHAT_TAG    : str

@dataclass
class ShopConfig:
    #CURRENCY: str
    DAY_PRICE                : float
    DEVICES_COUNT            : int

    TRIAL_ENABLED            : bool
    TRIAL_PERIOD             : int

    REFERRED_TRIAL_ENABLED   : bool
    REFERRED_TRIAL_PERIOD    : int

    REFERRER_REWARD_ENABLED  : bool
    REFERRER_REWARD_PERIOD   : int

    PAYMENT_STARS_ENABLED    : bool
    PAYMENT_CRYPTOMUS_ENABLED: bool
    PAYMENT_HELEKET_ENABLED  : bool
    PAYMENT_YOOKASSA_ENABLED : bool

@dataclass
class RemnaWaveConfig:
    
    PANEL_URL:str

    USERNAME: str
    PASSWORD: str

    TOKEN: str | None
    
    SUBSCRIPTION_PORT: int
    SUBSCRIPTION_PATH: str

@dataclass
class YooKassaConfig:
    TOKEN: str | None
    SHOP_ID: int | None

@dataclass
class DatabaseConfig:
    HOST    : str | None
    PORT    : int | None
    NAME    : str
    USERNAME: str | None
    PASSWORD: str | None

    def url(self, driver: str = "postgresql+asyncpg") -> str:
        # if driver.startswith("sqlite"):
        #     return f"{driver}:////{DEFAULT_DATA_DIR}/{self.NAME}.{DB_FORMAT}"
        return f"{driver}://{self.USERNAME}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"

@dataclass
class RedisConfig:
    HOST: str
    PORT: int
    DB_NAME: str
    USERNAME: str | None
    PASSWORD: str | None

    def url(self) -> str:
        if self.USERNAME and self.PASSWORD:
            return f"redis://{self.USERNAME}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB_NAME}"
        return f"redis://{self.HOST}:{self.PORT}/{self.DB_NAME}"

@dataclass
class LoggingConfig:
    LEVEL: str
    FORMAT: str
    ARCHIVE_FORMAT: str

@dataclass
class Config:
    bot         : BotConfig
    shop        : ShopConfig
    remnawave   : RemnaWaveConfig
    yookassa    : YooKassaConfig
    database    : DatabaseConfig
    redis       : RedisConfig
    logging     : LoggingConfig


def load_bot_config(env: Env):
    if True: # load
        TOKEN       = env.str ("BOT_TOKEN")
        BOT_VPN_NAME= env.str ("BOT_VPN_NAME") 
        ADMINS      = env.list("BOT_ADMINS", subcast=int, default=[], required=False)
        CHANNEL_TAG = env.str ("BOT_CHANNEL_TAG")
        CHAT_TAG    = env.str ("BOT_CHAT_TAG")
        DEV_ID      = env.int ("BOT_DEV_ID")
        SUPPORT_ID  = env.int ("BOT_SUPPORT_ID")
        DOMAIN      = env.str ("BOT_DOMAIN")
        PORT        = env.int ("BOT_PORT")

    if True: # warn
        if not TOKEN:
            logger.warning("BOT_TOKEN is not set")
        if not ADMINS:
            logger.warning("BOT_ADMINS list is empty.")
        if not SUPPORT_ID:
            logger.warning("BOT_SUPPORT_ID is not set")
        if not DOMAIN:
            logger.warning("BOT_DOMAIN is not set")
        if not PORT:
            logger.warning("BOT_PORT is not set")
        if not DEV_ID:
            logger.warning("DEV_ID is not set")
        if not BOT_VPN_NAME:
            logger.warning("BOT_NAME is not set")
        if not CHANNEL_TAG:
            logger.warning("CHANNEL_TAG is not set")
        if not CHAT_TAG:
            logger.warning("CHAT_TAG is not set")


    return BotConfig(
        TOKEN       = TOKEN,
        ADMINS      = ADMINS,
        SUPPORT_ID  = SUPPORT_ID, 
        DOMAIN      = DOMAIN,
        PORT        = PORT,
        DEV_ID      = DEV_ID,
        BOT_VPN_NAME= BOT_VPN_NAME,     #TODO: MOVE THAT TO SHOP_CONFIG
        CHANNEL_TAG = CHANNEL_TAG,      #TODO: MOVE THAT TO SHOP_CONFIG
        CHAT_TAG    = CHAT_TAG,         #TODO: MOVE THAT TO SHOP_CONFIG
        )

def load_shop_config(env: Env):
    if True:# load 
        DEVICES_COUNT             = env.int     ("SHOP_DEVICES_COUNT")

        TRIAL_ENABLED             = env.bool    ("SHOP_TRIAL_ENABLED")
        TRIAL_PERIOD              = env.int     ("SHOP_TRIAL_PERIOD")

        REFERRED_TRIAL_ENABLED    = env.bool    ("SHOP_REFERRED_TRIAL_ENABLED")
        REFERRED_TRIAL_PERIOD     = env.int     ("SHOP_REFERRED_TRIAL_PERIOD")

        REFERRER_REWARD_ENABLED   = env.bool    ("SHOP_REFERRER_REWARD_ENABLED")
        REFERRER_REWARD_PERIOD    = env.int     ("SHOP_REFERRER_REWARD_PERIOD")

        PAYMENT_STARS_ENABLED     = env.bool    ("SHOP_PAYMENT_STARS_ENABLED")
        PAYMENT_CRYPTOMUS_ENABLED = env.bool    ("SHOP_PAYMENT_CRYPTOMUS_ENABLED")
        PAYMENT_HELEKET_ENABLED   = env.bool    ("SHOP_PAYMENT_HELEKET_ENABLED")
        PAYMENT_YOOKASSA_ENABLED  = env.bool    ("SHOP_PAYMENT_YOOKASSA_ENABLED")
        DAY_PRICE                 = 3.33
    if True: #warn if not set
        if not DEVICES_COUNT:
            logger.warning("SHOP_DEVICES_COUNT is not set.")
        if not TRIAL_ENABLED:
            logger.warning("SHOP_TRIAL_ENABLED is not set.")
        if not TRIAL_PERIOD:
            logger.warning("SHOP_TRIAL_PERIOD is not set.")
        if not REFERRED_TRIAL_ENABLED:
            logger.warning("SHOP_REFERRED_TRIAL_ENABLED is not set.")
        if not REFERRED_TRIAL_PERIOD:
            logger.warning("SHOP_REFERRED_TRIAL_PERIOD is not set.")
        if not REFERRER_REWARD_ENABLED:
            logger.warning("SHOP_REFERRER_REWARD_ENABLED is not set.")
        if not REFERRER_REWARD_PERIOD:
            logger.warning("SHOP_REFERRER_REWARD_PERIOD is not set.")
        if not PAYMENT_STARS_ENABLED:
            logger.warning("SHOP_PAYMENT_STARS_ENABLED is not set.")
        if not PAYMENT_CRYPTOMUS_ENABLED:
            logger.warning("SHOP_PAYMENT_CRYPTOMUS_ENABLED is not set.")
        if not PAYMENT_HELEKET_ENABLED:
            logger.warning("SHOP_PAYMENT_HELEKET_ENABLED is not set.")
        if not PAYMENT_YOOKASSA_ENABLED:
            logger.warning("SHOP_PAYMENT_YOOKASSA_ENABLED is not set.")

    return ShopConfig(  
                        DEVICES_COUNT             = DEVICES_COUNT,
                        TRIAL_ENABLED             = TRIAL_ENABLED,
                        TRIAL_PERIOD              = TRIAL_PERIOD,
                        REFERRED_TRIAL_ENABLED    = REFERRED_TRIAL_ENABLED,
                        REFERRED_TRIAL_PERIOD     = REFERRED_TRIAL_PERIOD,
                        REFERRER_REWARD_ENABLED   = REFERRER_REWARD_ENABLED,
                        REFERRER_REWARD_PERIOD    = REFERRER_REWARD_PERIOD,
                        PAYMENT_STARS_ENABLED     = PAYMENT_STARS_ENABLED,
                        PAYMENT_CRYPTOMUS_ENABLED = PAYMENT_CRYPTOMUS_ENABLED,
                        PAYMENT_HELEKET_ENABLED   = PAYMENT_HELEKET_ENABLED,
                        PAYMENT_YOOKASSA_ENABLED  = PAYMENT_YOOKASSA_ENABLED,
                        DAY_PRICE                 = DAY_PRICE
                )

def load_remnawave_config(env: Env):
    if True: # load
        PANEL_URL         = env.str("REMNAWAVE_PANEL_URL")
        USERNAME          = env.str("REMNAWAVE_USERNAME")
        PASSWORD          = env.str("REMNAWAVE_PASSWORD")
        TOKEN             = env.str("REMNAWAVE_TOKEN")
        SUBSCRIPTION_PORT = env.int("REMNAWAVE_SUBSCRIPTION_PORT")
        SUBSCRIPTION_PATH = env.str("REMNAWAVE_SUBSCRIPTION_PATH")
    if True: # warn
        if not PANEL_URL:
            logger.warning("REMNAWAVE_PANEL_URL is not set.")
        if not USERNAME:
            logger.warning("REMNAWAVE_USERNAME is not set.")
        if not PASSWORD:
            logger.warning("REMNAWAVE_PASSWORD is not set.")
        if not TOKEN:
            logger.warning("REMNAWAVE_TOKEN is not set.")
        if not SUBSCRIPTION_PORT:
            logger.warning("REMNAWAVE_SUBSCRIPTION_PORT is not set.")
        if not SUBSCRIPTION_PATH:
            logger.warning("REMNAWAVE_SUBSCRIPTION_PATH is not set.")

    return RemnaWaveConfig(
                    PANEL_URL           = PANEL_URL,
                    USERNAME            = USERNAME,
                    PASSWORD            = PASSWORD,
                    TOKEN               = TOKEN,
                    SUBSCRIPTION_PORT   = SUBSCRIPTION_PORT,
                    SUBSCRIPTION_PATH   = SUBSCRIPTION_PATH,
                    )
    
def load_yookassa_config(env: Env):
    TOKEN   = env.str("YOOKASSA_TOKEN")
    SHOP_ID = env.str("YOOKASSA_SHOP_ID")

    if not TOKEN:
        logger.warning(TOKEN)
    if not SHOP_ID:
        logger.warning(SHOP_ID)

    return YooKassaConfig(TOKEN=TOKEN,
                          SHOP_ID=SHOP_ID)

def load_database_config(env: Env):
    HOST     = env.str("DATABASE_HOST")        
    PORT     = env.int("DATABASE_PORT")        
    NAME     = env.str("DATABASE_NAME")        
    USERNAME = env.str("DATABASE_USERNAME")
    PASSWORD = env.str("DATABASE_PASSWORD")

    if not HOST:
        logger.warning("DATABASE_HOST is not set.")
    if not PORT:
        logger.warning("DATABASE_PORT is not set.")
    if not NAME:
        logger.warning("DATABASE_NAME is not set.")
    if not USERNAME:
        logger.warning("DATABASE_USERNAME is not set.")
    if not PASSWORD:
        logger.warning("DATABASE_PASSWORD is not set.")
    
    return DatabaseConfig(
                        HOST = HOST,
                        PORT = PORT,
                        NAME = NAME,
                        USERNAME = USERNAME,
                        PASSWORD = PASSWORD,
    )

def load_redis_config(env: Env):
    HOST     = env.str("REDIS_HOST")
    PORT     = env.int("REDIS_PORT")
    DB_NAME  = env.str("REDIS_DB_NAME")
    USERNAME = env.str("REDIS_USERNAME")
    PASSWORD = env.str("REDIS_PASSWORD")
    
    if not HOST:
        logger.warning("REDIS_HOST is not set.")
    if not PORT:
        logger.warning("REDIS_PORT is not set.")
    if not DB_NAME:
        logger.warning("REDIS_NAME is not set.")
    if not USERNAME:
        logger.warning("REDIS_USERNAME is not set.")
    if not PASSWORD:
        logger.warning("REDIS_PASSWORD is not set.")

    return RedisConfig(
                        HOST = HOST,
                        PORT = PORT,
                        DB_NAME = DB_NAME,
                        USERNAME = USERNAME,
                        PASSWORD = PASSWORD,
    )

def load_logging_config(env: Env):
    LEVEL           = env.str("LOG_LEVEL")
    FORMAT          = env.str("LOG_FORMAT")
    ARCHIVE_FORMAT  = env.str("LOG_ARCHIVE_FORMAT") 
    if not LEVEL:
        logger.warning("LOG_LEVEL is not set")
    if not FORMAT:
        logger.warning("LOG_FORMAT is not set")
    if not ARCHIVE_FORMAT:
        logger.warning("LOG_ARCHIVE_FORMAT is not set")
    return LoggingConfig(LEVEL = LEVEL,
                         FORMAT = FORMAT,
                         ARCHIVE_FORMAT=ARCHIVE_FORMAT)

def load_config()-> Config:
    env = Env()
    env.read_env()

    bot             = load_bot_config       (env)
    shop            = load_shop_config      (env)
    remnawave       = load_remnawave_config (env)
    yookassa        = load_yookassa_config  (env)
    database        = load_database_config  (env)
    redis           = load_redis_config     (env)
    logging         = load_logging_config   (env)

    return Config(
        bot             = bot ,
        shop            = shop ,
        remnawave       = remnawave ,
        yookassa        = yookassa ,
        database        = database ,
        redis           = redis ,
        logging         = logging ,
    )
