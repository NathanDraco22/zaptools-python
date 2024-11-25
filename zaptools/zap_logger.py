import logging
from rich.logging import RichHandler


FORMAT = "%(message)s"
class ZapLogger():
    def __init__(self):
        logging.basicConfig(
             level= logging.INFO, 
             format=FORMAT, datefmt="[%X]", 
             handlers=[RichHandler(rich_tracebacks=True)]
        )
        self.logger = logging.getLogger('zap_logger')
    
    def info(self, message):
        self.logger.info(f"[Zap]{message}")
    
    def info_green(self, message):
        self.logger.info(f"[green][Zap]{message}", extra={"markup": True})
    
    def warning(self, message):
        self.logger.warning(f"[yellow][Zap]{message}", extra={"markup": True})
    
    def error(self, message):
        self.logger.error(f"[red][Zap]{message}", extra={"markup": True})


zap_logger = ZapLogger()


