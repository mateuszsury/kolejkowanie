import random
import numpy as np

class SystemMG1:
    def __init__(self):
        self.bufor = []
        self.czasy_obsługi = []

    def generuj_przyjazd(self):
        return random.expovariate(1 / 120)

    def generuj_czas_obsługi(self, rozkład):
        if rozklad == 'staly':
            return 60
        elif rozklad == 'jednostajny':
            return random.uniform(0, 120)
        elif rozklad == 'wykladniczy':
            return random.expovariate(1 / 60)
        elif rozklad == 'normalny':
            return max(0, random.normalvariate(60, 20))
        else:
            raise ValueError("Nieprawidłowy rodzaj rozkładu")

    def symuluj(self, liczba_iteracji, rozklad_obslugi):
        calkowity_czas_w_buforze = 0

        for _ in range(liczba_iteracji):
            # Generuj czas przyjazdu
            czas_przyjazdu = self.generuj_przyjazd()

            # Obsługa przyjazdów i odjazdów
            if not self.bufor:
                # Bufor jest pusty, obsługa rozpoczyna się natychmiast
                czas_obslugi = self.generuj_czas_obsługi(rozklad_obslugi)
                czas_odjazdu = czas_przyjazdu + czas_obslugi
                calkowity_czas_w_buforze += czas_obslugi
            else:
                # Bufor nie jest pusty, dodaj przyjazd do kolejki
                self.bufor.append(czas_przyjazdu)
                continue

            # Sprawdź, czy w buforze są oczekujące przyjazdy
            while self.bufor and self.bufor[0] < czas_odjazdu:
                # Obsłuż następny przyjazd z bufora
                czas_przyjazdu = self.bufor.pop(0)
                czas_obslugi = self.generuj_czas_obsługi(rozklad_obslugi)
                czas_odjazdu = czas_przyjazdu + czas_obslugi
                calkowity_czas_w_buforze += (czas_odjazdu - czas_przyjazdu)

        # Oblicz średni czas w buforze
        średni_czas_w_buforze = calkowity_czas_w_buforze / liczba_iteracji
        return średni_czas_w_buforze

system = SystemMG1()
sredni_czas = []

for i, rozklad in enumerate(['staly', 'jednostajny', 'wykladniczy', 'normalny']):
    sredni_czas.append(system.symuluj(1000, rozklad))
print(f"Średni czas przebywania zgłoszenia w buforze dla rozkładu [stały, jednostajny, wykładniczy, normalny]: {sredni_czas}")
