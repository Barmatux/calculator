from unittest import TestCase, mock
import argparse
from calculator.pycalc import read_consol


class TestRead_consol(TestCase):

    @mock.patch('argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(EXPRESSION=['2+2']))
    def test_read_consol(self, mock):
        self.assertEqual(read_consol(), '2+2')

    @mock.patch('argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(EXPRESSION=['2 + 2']))
    def test_read_consol_with_wht_spaces(self, mock):
        self.assertEqual(read_consol(), '2 + 2')


    @mock.patch('argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(EXPRESSION=['-6+3']))
    def test_read_consol_negative_value(self, mock):
        self.assertEqual(read_consol(), '-6+3')

    @mock.patch('argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(EXPRESSION=['']))
    def test_read_consol_none(self, mock):
        self.assertEqual(read_consol(), '')