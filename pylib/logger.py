import logging
import logging.handlers

LoggingLevel = logging.DEBUG
LOG_PATH = 'log/status.log'


def setup_logger(logger):
    """
    Set up a specific logger - logger
    """
    logger.setLevel(LoggingLevel)
    log_path = LOG_PATH
    handler = logging.handlers.TimedRotatingFileHandler(log_path,
                                                        when='d',
                                                        interval=1)
    handler.setLevel(LoggingLevel)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


logger = logging.getLogger('error')
setup_logger(logger)
