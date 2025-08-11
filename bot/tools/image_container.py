

from dataclasses import dataclass
import logging

from aiogram.types import FSInputFile

from modules.bot.utils.navigation import NavNotify


logger = logging.getLogger(__name__)

@dataclass
class ImageContainer():
    connect             : FSInputFile
    invite              : FSInputFile
    notify              : FSInputFile
    main_menu           : FSInputFile
    purschare           : FSInputFile
    purschare_success   : FSInputFile
    service             : FSInputFile
    support             : FSInputFile

def load_images() -> ImageContainer:

    connect                         = FSInputFile("src/connect.JPEG")
    invite                          = FSInputFile("src/invite.JPEG")
    notify                          = FSInputFile("src/notify.JPEG")
    main_menu                       = FSInputFile("src/main_menu.JPEG")
    purschare                       = FSInputFile("src/purschare.JPEG")
    purschare_success               = FSInputFile("src/purschare_success.JPEG")
    service                         = FSInputFile("src/service.JPEG")
    support                         = FSInputFile("src/support.JPEG")
    
    logger.info("images loaded")
    return ImageContainer(
        connect             = connect,
        invite              = invite,
        notify              = notify,
        main_menu           = main_menu,
        purschare           = purschare ,
        purschare_success   = purschare_success,
        service             = service,
        support             = support

    )
