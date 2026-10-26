import unittest
from queue_model import SystemMG1

class QueueTests(unittest.TestCase):
    def test_overlapping_arrivals_wait_for_the_previous_departure(self):
        model = SystemMG1()
        arrivals = iter([0, 30, 90])
        model.generuj_przybycie = lambda: next(arrivals)
        self.assertEqual(model.symuluj(3, 'staly', warmup=0), 70)
        self.assertEqual(model.last_result['mean_wait'], 10)

    def test_md1_matches_analytical_steady_state(self):
        model = SystemMG1(seed=42)
        self.assertAlmostEqual(model.symuluj(100000, 'staly'), 90, delta=4)

    def test_service_argument_does_not_depend_on_module_globals(self):
        self.assertEqual(SystemMG1().generuj_czas_obsługi('staly'), 60)

    def test_empty_observations_rejected(self):
        with self.assertRaises(ValueError):
            SystemMG1().symuluj(0, 'staly')

if __name__ == '__main__':
    unittest.main()
