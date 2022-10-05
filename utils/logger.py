import logging
from ..config import log_level,has_file_handler

class Logger:

    def __init__(self,filename,log_level=log_level,has_file_handler=has_file_handler):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        self.logger.addHandler(console_handler)

        if has_file_handler:
            file_handler = logging.FileHandler(f'{__name__}_{filename}.log', 'a')
            file_handler.setLevel(log_level)
            self.logger.addHandler(file_handler)
