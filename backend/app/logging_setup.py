import logging
import logging.handlers
import time

class LoggerSetup:
    
    def __init__(self) -> None:
        self.logger = logging.getLogger('')
        self.setup_logging()
        
    def setup_logging(self):
        # add log format
        LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
        
        # configure formatter for logger
        formatter = logging.Formatter(LOG_FORMAT)
        
        # configure console handler
        console= logging.StreamHandler()
        console.setFormatter(formatter)
        
        # Configure TimeRotatingFileHandler
        log_file = "logs/carib-efk.log"
        file = logging.handlers.TimedRotatingFileHandler(filename=log_file, when="midnight", backupCount=5)
        file.setFormatter(formatter)
        