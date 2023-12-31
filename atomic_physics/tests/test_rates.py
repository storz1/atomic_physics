"""Test Rates Calculations"""
import unittest
import atomic_physics as ap
from atomic_physics.ions import ca43


def _steady_state_population(intensity: float):
    "Steady state population in the P-state for resonant intensity /I0"
    return intensity / (2 * intensity + 1)


class TestTSS(unittest.TestCase):
    """Two-state system tests

    The closed stretch cycling transition is used to make a two state system"""

    def test_rates_relations(self):
        """Test the spontaneous rates satisfy relations in net rates

        This relation is used in the steady states tests."""
        intensity_list = [1e-3, 1e-1, 0.3, 1, 1.0, 2, 10.0, 1.2e4]

        ion = ca43.Ca43(B=5e-4, level_filter=[ca43.ground_level, ca43.P32])
        s_idx = ion.index(ca43.ground_level, 4)
        p_idx = ion.index(ca43.P32, +5)

        rates = ap.rates.Rates(ion)
        delta = ion.delta(s_idx, p_idx)
        for I in intensity_list:
            Lasers = [ap.Laser("393", q=+1, I=I, delta=delta)]  # resonant
            trans = rates.get_transitions(Lasers)

            spont = rates.get_spont()
            r = spont[p_idx, p_idx] / (trans[p_idx, p_idx] + trans[p_idx, s_idx])
            self.assertAlmostEqual(r, 1.0, places=7)

    def test_steady_state_intensity(self):
        """Test the steady state intensity scaling"""

        # use both integers and floats
        intensity_list = [1e-3, 1e-1, 0.3, 1, 1.0, 2, 10.0, 1.2e4]

        ion = ca43.Ca43(B=5e-4, level_filter=[ca43.ground_level, ca43.P32])
        s_idx = ion.index(ca43.ground_level, 4)
        p_idx = ion.index(ca43.P32, +5)

        rates = ap.rates.Rates(ion)
        delta = ion.delta(s_idx, p_idx)

        for I in intensity_list:
            Lasers = [ap.Laser("393", q=+1, I=I, delta=delta)]  # resonant
            trans = rates.get_transitions(Lasers)

            Np_ss = _steady_state_population(I)
            # transition rates normalised by A coefficient
            dNp_dt = trans[p_idx, p_idx] * Np_ss + trans[p_idx, s_idx] * (1 - Np_ss)
            dNp_dt = dNp_dt / (trans[p_idx, p_idx] + trans[p_idx, s_idx])
            self.assertAlmostEqual(0.0, dNp_dt, places=7)
            dNs_dt = trans[s_idx, p_idx] * Np_ss + trans[s_idx, s_idx] * (1 - Np_ss)
            dNs_dt = dNs_dt / (trans[s_idx, p_idx] + trans[s_idx, s_idx])
            self.assertAlmostEqual(0.0, dNs_dt, places=7)

    def test_steady_state_detuning(self):
        """Test steady state detuning dependence"""

        # assume 1 saturation intensity
        ion = ca43.Ca43(B=5e-4, level_filter=[ca43.ground_level, ca43.P32])
        s_idx = ion.index(ca43.ground_level, 4)
        p_idx = ion.index(ca43.P32, +5)

        rates = ap.rates.Rates(ion)
        delta = ion.delta(s_idx, p_idx)

        Lasers = [ap.Laser("393", q=+1, I=1.0, delta=delta)]  # resonant
        trans = rates.get_transitions(Lasers)
        line_width = abs(trans[p_idx, p_idx] + trans[p_idx, s_idx])

        # detuning scan relative to linewidth
        norm_detuning = [-1e4, 2.3e1, 2, -4, 0.5, 0]
        for det in norm_detuning:
            I_eff = 1 / (4 * det**2 + 1)
            Np_ss = _steady_state_population(I_eff)

            Lasers = [ap.Laser("393", q=+1, I=1.0, delta=delta + line_width * det)]
            trans = rates.get_transitions(Lasers)

            # transition rates normalised by A coefficient
            dNp_dt = trans[p_idx, p_idx] * Np_ss + trans[p_idx, s_idx] * (1 - Np_ss)
            dNp_dt = dNp_dt / (trans[p_idx, p_idx] + trans[p_idx, s_idx])
            self.assertAlmostEqual(0.0, dNp_dt, places=7)
            dNs_dt = trans[s_idx, p_idx] * Np_ss + trans[s_idx, s_idx] * (1 - Np_ss)
            dNs_dt = dNs_dt / (trans[s_idx, p_idx] + trans[s_idx, s_idx])
            self.assertAlmostEqual(0.0, dNs_dt, places=7)


if __name__ == "__main__":
    unittest.main()
