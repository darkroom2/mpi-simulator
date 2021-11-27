from itertools import product
from json import loads, JSONDecodeError
from logging import info
from pathlib import Path

from numpy.random import default_rng

from simulator.simulator import Simulator
from simulator.utils import setup_logger, get_max_traffic


class Simulation:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = self.load_config(config_path)

    @staticmethod
    def load_config(path):
        """Parse json file to dict."""

        config_file = Path(path)
        try:
            return loads(config_file.read_text(encoding='utf8'))
        except JSONDecodeError:
            return {}

    def run(self):

        # TODO: Wykresy zależności że np. P_block nie zmienia sie liniowo ze
        #  wzrostem serwerow itp. ze wynik jest niezalezny od roznych rozkladow
        #  czasu obslugi

        mi_values = self.config.get('mi_values', [1])
        server_counts = self.config.get('server_counts', [5])
        target_probabilities = self.config.get('blocking_probabilities', [0.2])
        sim_repetitions = self.config.get('simulation_repetitions', 10)
        time_limit = self.config.get('time_limit', 999)
        events_limit = self.config.get('events_limit', 500000)
        seed = self.config.get('seed', 123)
        show_plots = self.config.get('show_plots', True)
        info('Simulation config loaded')

        rng = default_rng(seed)
        info(f'Initializing rng with seed = {seed}')

        combinations = product(target_probabilities, mi_values, server_counts)
        results_for_combinations = []

        info(f'Running simulator with k = {sim_repetitions} repetitions for '
             f'each combination of μ values, server counts and target '
             f'probabilities')
        for target_probability, mi, servers in combinations:
            target_rho = get_max_traffic(target_probability, servers,
                                         show_plot=show_plots)
            info(f'Max traffic ϱ = {target_rho}, for N = {servers} servers and '
                 f'P_block = {target_probability}')

            lam = mi * target_rho
            info(f'Calculated λ = {lam} for μ = {mi}')

            simulator_results = []

            for i in range(sim_repetitions):
                info(f'Running #{i + 1} simulation')
                sim = Simulator(lam=lam, mi=mi, servers=servers,
                                time_limit=time_limit,
                                events_limit=events_limit,
                                seed=rng.integers(999999))
                sim.run()

                simulated_probability = sim.get_result()
                info(f'Simulated P_block = {simulated_probability}')

                simulator_results.append(simulated_probability)

            results_for_combinations.append(simulator_results)

        info(f'{results_for_combinations}')


def main():
    """Testing simulator."""

    logger = setup_logger()

    logger.info('Starting simulation')

    # TODO: argparse
    sim = Simulation('config/config.json')
    sim.run()


if __name__ == '__main__':
    main()
