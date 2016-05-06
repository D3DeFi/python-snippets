import logging


LOG_HANDLER = logging.StreamHandler()
LOG_HANDLER.setFormatter(logging.Formatter('%(asctime)s %(name)s %(message)s'))
LOG_HANDLER.setLevel(logging.DEBUG)


class Logger():
    """Provides wrapper for loggin.Logger object with option to set logging level across
    all existing instances of Logger class via their shared logging.StreamHandler."""

    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.addHandler(LOG_HANDLER)
        self.logger.setLevel(logging.DEBUG)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)

    def setLevel(self, lvl):
        log_level = getattr(logging, lvl, None)
        if log_level:
            self.logger.setLevel(log_level)
            LOG_HANDLER.setLevel(log_level)
