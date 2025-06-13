import logging


class LogFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()

        blue = "\033[0;34m"
        yellow = "\033[0;33m"
        red = "\033[0;31m"
        red_bg = "\033[0;101m"
        black = "\033[0;90m"
        purple = "\033[0;35m"
        reset = "\033[0m"

        level_colour_mapping = [
            (logging.DEBUG, reset),
            (logging.INFO, blue),
            (logging.WARNING, yellow),
            (logging.ERROR, red),
            (logging.CRITICAL, red_bg),
        ]

        time = f"{black}%(asctime)s{reset}"
        name = f"{purple}%(name)s{reset}"
        message = f"%(message)s{reset}"
        level_name = f"%(levelname)-8s{reset}"

        date_format = "%Y-%m-%d %H:%M:%S"

        self._formatters = {
            level: logging.Formatter(f"{time} {colour}{level_name} {name}: {message}", date_format)
            for (level, colour) in level_colour_mapping
        }

    def format(self, record):
        return self._formatters[record.levelno].format(record)
