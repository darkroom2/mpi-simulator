from logging import info
from time import time
from typing import List, Tuple

from numpy.random import default_rng


class Simulator:
    def __init__(self, lam, mi, servers: int, max_time: float):
        self.lam = lam  # Lambda
        self.mi = mi  # Mi
        self.servers = servers  # Number of servers
        self.max_time = max_time  # Simulation time
        self.busy = 0  # Busy servers counter
        self.start_time = 0  # Simulation start time
        self.arrivals = 0  # Incoming packet counter
        self.blocked = 0  # Rejected packet counter
        self.served = 0  # Handled packet counter
        self.event_list: List[Tuple] = []  # Event list
        self.rng = default_rng()  # Random number generator

    def end(self):
        """End simulation condition."""

        return time() - self.start_time > self.max_time

    def run(self):
        """Run simulation."""

        info('Starting simulation')
        self.start_time = time()

        # Add primary event on list
        ev = ('arrival', self.start_time)
        self.event_list.append(ev)
        self.arrivals += 1
        info(f'Adding to event list {ev}')

        while not self.end():
            # Take event from list
            ev = self.pop_list()
            ev_type, ev_time = ev
            info(f'New event appeared {ev}')

            if ev_type == 'arrival':
                if not self.servers_busy():
                    new_ev2 = (f'end_of_service_{self.busy + 1}', ev_time + self.serve_time())
                    self.event_list.append(new_ev2)
                    info(f'Adding to event list {new_ev2}')
                    self.busy += 1
                else:
                    self.blocked += 1

            elif 'end_of_service' in ev_type:
                self.served += 1
                self.busy -= 1

            new_ev = ('arrival', ev_time + self.arrival_time())
            self.event_list.append(new_ev)
            self.arrivals += 1
            info(f'Adding to event list {new_ev}')
            info(f'arv={self.arrivals}, '
                 f'bsy={self.busy}, '
                 f'srvd={self.served}, '
                 f'blck={self.blocked}, '
                 f'P_block={self.blocked / self.arrivals}')

    def pop_list(self):
        """Returns next to come event."""

        # Sort ascending by time
        self.event_list.sort(key=lambda x: x[1])
        # Take event with smallest time
        ev = self.event_list[0]
        # Remove it from list by overwriting list bypassing zero element
        self.event_list = self.event_list[1:]
        # Return the event
        return ev

    def serve_time(self):
        """Generate serving time."""

        return self.rng.exponential(1 / self.mi)

    def arrival_time(self):
        """Generate arrival time."""

        return self.rng.exponential(1 / self.lam)

    def servers_busy(self):
        """Check if server is busy by comparing number of end_of_service events with number of servers."""

        return self.busy == self.servers
