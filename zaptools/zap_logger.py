import logging
from rich.logging import RichHandler


class ZapLogger:
    def __init__(self):
        self.logger = logging.getLogger("zap_logger")
        self.logger.addHandler(
            RichHandler(
                markup=True,
                rich_tracebacks=True,
                show_path=False,
            )
        )
        self.logger.setLevel(logging.INFO)

    def info(self, message: str):
        self.logger.info(f"[Zap]{message}")

    def info_green(self, message: str):
        self.logger.info(f"[green][Zap]{message}", extra={"markup": True})

    def warning(self, message: str):
        self.logger.warning(f"[yellow][Zap]{message}", extra={"markup": True})

    def error(self, message: str):
        self.logger.error(f"[red][Zap]{message}", extra={"markup": True})


zap_logger = ZapLogger()
