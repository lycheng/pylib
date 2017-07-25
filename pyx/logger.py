import logging
import logging.handlers

LoggingLevel = logging.DEBUG


def get_default_logger(name="default"):
    """ return a default logger for stdout

    Args:
        name: string, for name of logger

    Returns:
        logger: logger
    """
    logger = logging.getLogger('default')

    print(logger)

    logger.setLevel(LoggingLevel)
    handler = logging.handlers.StreamHandler()
    handler.setLevel(LoggingLevel)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
