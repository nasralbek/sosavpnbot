from enum import Enum



TELEGRAM_WEBHOOK = "/webhook"

LOG_ZIP_ARCHIVE_FORMAT = "zip"
LOG_GZ_ARCHIVE_FORMAT = "gz"


class TransactionStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELED = "canceled"
    REFUNDED = "refunded"



MAIN_MESSAGE_ID_KEY     = 'main_message_id'
PREVIOUS_CALLBACK_KEY   = "previous_callback"
PREVIOUS_MESSAGE_ID_KEY = 'previous_message_id' 


DEFAULT_LANGUAGE    = "ru"
I18N_DOMAIN         = "bot"