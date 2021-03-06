import unittest

from twittero import Twittero

class TestAmbito(unittest.TestCase):

    def test_postear_en_dlm(self):
        t = Twittero()
        t.postear_en_dlm(fecha='20200911', diario='clarin', secciones='politica-economia-sociedad')

    def test_postear_en_discursosdeaf(self):
        t = Twittero()
        t.postear_en_discursosdeaf(fecha='20200914')

    def test_postear_en_discursoshistoricos(self):
        t = Twittero()
        t.postear_en_discursoshistoricos('discursosdenk')
