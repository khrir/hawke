from logging.handlers import RotatingFileHandler
import logging, os

class FileLogWriter:
    def __init__(self):
        self.log_dir = 'logs'
        os.makedirs(self.log_dir, exist_ok=True)

        self._setup_logger('debug', 'debug.log', logging.DEBUG)
        self._setup_logger('error', 'error.log', logging.ERROR)
        self._setup_logger('purchase', 'purchase.log', logging.INFO)

    def _setup_logger(self, name, filename, level):
        logger = logging.getLogger(name)
        logger.setLevel(level)

        handler = RotatingFileHandler(
            os.path.join(self.log_dir, filename), maxBytes=5000, backupCount=3
        )
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(handler)
        setattr(self, f"{name}_logger", logger)

    def debug(self, message):
        """Log de debug"""
        self.debug_logger.debug(message)

    def error(self, message):
        """Log de erro"""
        self.error_logger.error(message)

    def purchase(self, message):
        """Log para compras"""
        self.purchase_logger.info(message)