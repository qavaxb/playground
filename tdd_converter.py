import unittest

COEFF_KM_TO_M_UNIT = 1000


class UnitConverter:

    def convert_km_to_m(self, length):
        if length < 0:
            raise ValueError('Input shall not be negative')
        return length * COEFF_KM_TO_M_UNIT


class TestUnitConverter(unittest.TestCase):

    def setUp(self):
        self.converter = UnitConverter()

    def test_km_c_m_negative_values(self):
        with self.assertRaises(ValueError):
            self.converter.convert_km_to_m(-1)

    def test_km_c_m_conversion(self):
        self.assertEqual(self.converter.convert_km_to_m(2), 2000)

    def test_km_c_m_arg_string(self):
        with self.assertRaises(TypeError):
            self.converter.convert_km_to_m('Eins')
