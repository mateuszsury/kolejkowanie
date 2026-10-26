"""Reproducible FCFS M/G/1 simulation; all times are in seconds."""
import math
import random


class SystemMG1:
    def __init__(self, seed=42):
        self._rng = random.Random(seed)
        self.last_result = None

    def generuj_losowa(self):
        return self._rng.random()

    def generuj_przybycie(self):
        return -120 * math.log1p(-self.generuj_losowa())

    def generuj_czas_obslugi(self, rozklad):
        if rozklad == 'staly':
            return 60.0
        if rozklad == 'jednostajny':
            return 120 * self.generuj_losowa()
        if rozklad == 'wykladniczy':
            return -60 * math.log1p(-self.generuj_losowa())
        if rozklad == 'normalny':
            u = 1 - self.generuj_losowa()
            z = math.sqrt(-2 * math.log(u)) * math.cos(2 * math.pi * self.generuj_losowa())
            return max(0, 60 + 20 * z)
        raise ValueError('Nieprawidlowy rodzaj rozkladu')

    # Preserve the original public spelling as a compatibility alias.
    def generuj_czas_obsługi(self, rozkład):
        return self.generuj_czas_obslugi(rozkład)

    def symuluj(self, liczba_iteracji, rozklad_obslugi, warmup=1000):
        if liczba_iteracji < 1 or warmup < 0:
            raise ValueError('Require at least one observation and nonnegative warmup')
        arrival = departure = waiting = system = 0.0
        for i in range(liczba_iteracji + warmup):
            arrival += self.generuj_przybycie()
            service = self.generuj_czas_obslugi(rozklad_obslugi)
            if service < 0:
                raise ValueError('Service duration must be nonnegative')
            start = max(arrival, departure)
            departure = start + service
            if i >= warmup:
                waiting += start - arrival
                system += departure - arrival
        self.last_result = {'mean_wait': waiting / liczba_iteracji,
                            'mean_system': system / liczba_iteracji,
                            'observations': liczba_iteracji, 'warmup': warmup}
        return self.last_result['mean_system']


def main(system_type=SystemMG1):
    for distribution in ['staly', 'jednostajny', 'wykladniczy', 'normalny']:
        model = system_type(seed=42)
        model.symuluj(100000, distribution)
        print(distribution, model.last_result)
