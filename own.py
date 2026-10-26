"""M/G/1 example using the original 32-bit linear congruential generator."""
from queue_model import SystemMG1 as BaseSystemMG1, main

class SystemMG1(BaseSystemMG1):
    def __init__(self, seed=42):
        super().__init__(seed)
        self.stan_losowy = seed

    def generuj_losowa(self):
        self.stan_losowy = (self.stan_losowy * 1664525 + 1013904223) % 2**32
        return self.stan_losowy / 2**32

if __name__ == '__main__':
    main(SystemMG1)
