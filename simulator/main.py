from simulator.simulator import Simulator
from simulator.utils import setup_logger


def main():
    setup_logger()
    sim = Simulator(lam=10, mi=5, servers=500, max_time=10)
    sim.run()


if __name__ == '__main__':
    main()
