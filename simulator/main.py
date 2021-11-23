from json import loads, JSONDecodeError
from pathlib import Path

from matplotlib.pyplot import plot, show, title
from numpy import arange, abs as np_abs

from simulator.simulator import Simulator
from simulator.utils import setup_logger, calculate_max_traffic, erlang_b, \
    find_closest, get_x_for_y


def get_config(path):
    """Parse json file to dict."""

    cfg_file = Path(path)
    try:
        return loads(cfg_file.read_text(encoding='utf8'))
    except JSONDecodeError:
        return {}


def main():
    """Testing simulator."""

    logger = setup_logger()

    config = get_config('config/config.json')

    servers = config.get('servers', 1)
    max_time = config.get('simulation_time', 1)
    target_probability = config.get('blocking_probability', 0)

    logger.info(f'Loaded config with values: servers = {servers}, '
                f'max_time = {max_time}, P_block = {target_probability}')

    erlangs = arange(0, 50, 0.00001)
    probabilities = erlang_b(erlangs, servers)

    target_rho = get_x_for_y(erlangs, probabilities, target_probability)

    logger.info(f'Calculated theoretical maximum traffic offered to a system '
                f'with N = {servers} servers and '
                f'P_block = {target_probability} equals: {target_rho}')

    sim = Simulator(lam=lam, mi=mi, servers=servers, max_time=max_time)
    sim.run()

    logger.info(f'Plotting Erlang function for N = {servers}')
    title(f'Erlang B formula for N = {servers}')
    plot(erlangs, probabilities)
    show()


if __name__ == '__main__':
    main()
