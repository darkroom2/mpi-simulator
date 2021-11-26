from json import loads, JSONDecodeError
from pathlib import Path

from simulator.simulator import Simulator
from simulator.utils import setup_logger, get_max_traffic


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

    # TODO: Wykresy zależności że np. P_block nie zmienia sie liniowo ze
    #  wzrostem serwerow itp.

    servers = config.get('servers', 5)
    # TODO: Dla roznych wartosci prawdopodobienst
    target_probability = config.get('blocking_probability', 0.2)
    show_plots = config.get('show_plots', True)

    # TODO: dla roznej liczby serwerow
    logger.info(f'Loaded config with values: servers = {servers}, '
                f'P_block = {target_probability}')

    target_rho = get_max_traffic(target_probability, servers,
                                 show_plot=show_plots)
    logger.info(f'Calculated max traffic ϱ = {target_rho}, for N = {servers} '
                f'servers and P_block = {target_probability}')

    lam = config.get('lam', 1)
    max_time = config.get('simulation_time', 5)
    max_events = config.get('max_events', 500000)
    # TODO: zmieniony seed dla kazdej k ∈ K
    seed = config.get('seed', 123)

    # TODO: mi zamienic na lam (w konfigu też)
    mi = lam / target_rho
    logger.info(f'Calculated μ = {mi} for simulation')

    logger.info(f'Running simulation to confirm the blocking probability of '
                f'P_block = {target_probability} for calculated traffic '
                f'ϱ = {target_rho} with loaded parameters: λ = {lam}, '
                f'μ = {mi}, max_time = {max_time}, max_events = {max_events}, '
                f'seed = {seed}')

    sim = Simulator(lam=lam, mi=mi, servers=servers, max_time=max_time,
                    max_events=max_events, seed=seed)
    sim.run()

    simulated_probability = sim.get_result()
    diff = abs(target_probability - simulated_probability)
    logger.info(f'Calculated absolute difference of simulated and calculated '
                f'blocking probabilities is: {diff}')


if __name__ == '__main__':
    main()
