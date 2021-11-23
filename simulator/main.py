from json import loads, JSONDecodeError
from pathlib import Path

from simulator.simulator import Simulator
from simulator.utils import setup_logger, calculate_max_traffic


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

    lam = config.get('lambda', 1)
    mi = config.get('mi', 1)
    servers = config.get('servers', 1)
    max_time = config.get('simulation_time', 1)
    blocking_probability = config.get('blocking_probability', 0)

    logger.info(f'Loaded config with values: lam = {lam}, mi = {mi}, '
                f'rho = {lam / mi}, servers = {servers},'
                f'max_time = {max_time}, P_block = {blocking_probability}')

    rho_by_formula = calculate_max_traffic(blocking_probability, servers)
    logger.info(f'Calculated theoretical maximum traffic offered to a system '
                f'with N = {servers} servers and '
                f'P_block = {blocking_probability} equals: {rho_by_formula}')

    sim = Simulator(lam=lam, mi=mi, servers=servers, max_time=max_time)
    sim.run()


if __name__ == '__main__':
    main()
