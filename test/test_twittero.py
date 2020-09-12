import unittest

from twittero import Twittero

class TestAmbito(unittest.TestCase):

    def test_frecuencia_todo(self):
        t = Twittero()
        t.postear_en_dlm(fecha='20200911', diario='clarin', categorias='politica-economia-sociedad')
