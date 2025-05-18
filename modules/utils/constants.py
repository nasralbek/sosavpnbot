from enum import Enum



TELEGRAM_WEBHOOK = "/webhook"

LOG_ZIP_ARCHIVE_FORMAT = "zip"
LOG_GZ_ARCHIVE_FORMAT = "gz"


class TransactionStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELED = "canceled"
    REFUNDED = "refunded"