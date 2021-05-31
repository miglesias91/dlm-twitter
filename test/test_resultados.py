import unittest

from resultados import Resultados

class TestAmbito(unittest.TestCase):

    def test_frecuencia_todo(self):
        r = Resultados()
        freqs = r.frecuencias(fecha='20200911', diario='clarin', secciones='politica', verbos=False)
        freqs
