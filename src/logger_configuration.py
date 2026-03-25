

import logging

class ColoredFormatter(logging.Formatter):
    # Codigos ANSI para colores en terminal (sin emojis)
    GREEN = "\x1b[32;20m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    RESET = "\x1b[0m"
    format_str = "%(asctime)s - %(levelname)s - %(message)s"

    FORMATS = {
        logging.INFO: GREEN + format_str + RESET,
        logging.WARNING: YELLOW + format_str + RESET,
        logging.ERROR: RED + format_str + RESET,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt='%H:%M:%S')
        return formatter.format(record)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(ColoredFormatter())
logger.addHandler(ch)
