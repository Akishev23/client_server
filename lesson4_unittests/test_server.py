import unittest
from lesson3_dk import server as s
from lesson3_dk.useful import functions as f
from lesson3_dk.useful.variables import RESPONSE, ERROR


class TestServer(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testprocescorrecctresponse(self):
        """checking correct response"""
        mes = f.say_hello()

        self.assertDictEqual(s.process_client_message(mes), {RESPONSE: 200})

    def testprocesbadresponse(self):
        """checking bad request"""
        bad = {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        }
        self.assertDictEqual(s.process_client_message(''), bad)

    def testpocessin(self):
        """checking if RESPONSE is in answer"""
        self.assertIn(RESPONSE, s.process_client_message(f.say_hello()))
