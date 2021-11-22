from json import loads
from pathlib import Path

from simulator.simulator import Simulator
from simulator.utils import setup_logger


def get_config(path):
    """Parse json file to dict."""

    cfg_file = Path(path)
    return loads(cfg_file.read_text(encoding='utf8'))


def main():
    """Testing simulator."""

    setup_logger()

    config = get_config('config/config.json')

    lam = config.get('lambda', 8)
    mi = config.get('mi', 8)
    servers = config.get('servers', 10)
    max_time = config.get('simulation_time', 10)

    sim = Simulator(lam=lam, mi=mi, servers=servers, max_time=max_time)
    sim.run()


if __name__ == '__main__':
    main()
