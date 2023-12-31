import unittest
import atomic_physics as ap
from atomic_physics.ions import ca43


class TestStim(unittest.TestCase):
    def test_multi_transition(self):
        """Test with lasers on multiple transitions (see #15)"""
        ion = ca43.Ca43(B=146e-4)
        rates = ap.rates.Rates(ion)
        Lasers = [
            ap.Laser("397", q=0, I=1, delta=0),
            ap.Laser("866", q=0, I=1, delta=0),
        ]
        rates.get_transitions(Lasers)

    def test_multi_laser(self):
        """Test with multiple lasers on one transition"""
        ion = ca43.Ca43(B=146e-4)
        rates = ap.rates.Rates(ion)
        Lasers = [
            ap.Laser("397", q=0, I=1, delta=0),
            ap.Laser("397", q=+1, I=1, delta=0),
        ]
        rates.get_transitions(Lasers)
