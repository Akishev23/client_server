import unittest
import time
from lesson3_dk.useful import functions as f
from lesson3_dk.useful.variables import ACTION, TIME, PRESENCE, USER, ACCOUNT_NAME

mes = {
    ACTION: PRESENCE,
    TIME: time.time(),
    USER: {
        ACCOUNT_NAME: 'guest'
    }
}


class TestFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testsayhelloin(self):
        """checking presence action in message"""
        self.assertIn(ACTION, f.say_hello())

    def testsayhelloeq(self):
        """checking message's equality to correct message"""
        self.assertDictEqual(f.say_hello(), mes)

    def testsayhelloeqs(self):
        """checking right user's name"""
        self.assertEquals(f.say_hello('denis')[USER][ACCOUNT_NAME], 'denis')

    def testcheckportbad(self):
        """checking out of use port answer"""
        self.assertEqual(f.check_port(3), 0)

    def testcheckportok(self):
        """checking correct port answer"""
        self.assertTrue(f.check_port(4353), True)
