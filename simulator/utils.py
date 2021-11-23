from logging import getLogger, INFO, Formatter, StreamHandler, FileHandler
from math import factorial


def setup_logger(level=INFO):
    """Configures logger with preset format."""

    _logger = getLogger()
    _logger.setLevel(level)

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


def calculate_max_traffic(p, n):
    """Find value of max traffic offered to the system for given loss
    probability and number of serving devices."""

    i = 0
    inc = 0.001
    while True:
        if erlang_b(n, i) >= p:
            return i
        i += inc


def erlang_b(servers, traffic):
    """Erlang's B formula. Used for dimensioning different types of networks."""

    numerator = traffic ** servers / factorial(servers)
    _sum = 0
    for i in range(0, servers + 1):
        _sum += (traffic ** i) / factorial(i)
    return numerator / _sum
