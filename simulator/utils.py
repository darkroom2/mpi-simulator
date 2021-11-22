from logging import getLogger, DEBUG, Formatter, StreamHandler, FileHandler


def setup_logger():
    """Configures logger with preset format."""

    _logger = getLogger()
    _logger.setLevel(DEBUG)

    formatter = Formatter(
        '%(asctime)s %(processName)s %(threadName)s - %(levelname)s - %('
        'message)s '
    )

    console_handler = StreamHandler()
    console_handler.setFormatter(formatter)
    _logger.addHandler(console_handler)

    file_handler = FileHandler('simulation.log')
    file_handler.setFormatter(formatter)
    _logger.addHandler(file_handler)

    return _logger
