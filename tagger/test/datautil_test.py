import unittest2
from StringIO import StringIO

import mock

from .. import datautil
import testsetup

class DataUtilTest(unittest2.TestCase):
    def setUp(self):
        self._data="""
            <s> <s>
            NNP Pierre
            NNP Vinken
            NNP Vinken
            , ,
            CD 61
            RB steadily
            VBG increasing
            NN net
            . ."""


        self._mock = testsetup.mock_open(data=StringIO(self._data))
        self._open_name = "{0}.open".format(datautil.__name__)

    def test_get_tag_word_matrix(self):
        expected = {"<s> <s>": 1, "Pierre NNP": 1, "Vinken NNP": 2,
                ", ,": 1, "61 CD": 1, "steadily RB": 1, "increasing VBG": 1,
                "net NN": 1, ". .": 1}

        with mock.patch(self._open_name, self._mock, create=True):
            actual = datautil.get_tag_word_matrix(filename="")

        self.assertEqual(expected, actual)

    def test_unigram(self):
        expected = {"<s>": 1, "NNP": 3, ",": 1, "CD": 1, "RB": 1, "VBG": 1,
                "NN": 1, ".": 1}

        with mock.patch(self._open_name, self._mock, create=True):
            actual = datautil.get_tag_n_gram(n=1, filename="")

        self.assertEqual(expected, actual)

    def test_bigram(self):
        expected = {"NNP <s>": 1, "NNP NNP": 2, ", NNP": 1, "CD ,":1,
                "RB CD": 1, "VBG RB": 1, "NN VBG": 1, ". NN": 1}

        with mock.patch(self._open_name, self._mock, create=True):
            actual = datautil.get_tag_n_gram(n=2, filename="")

        self.assertEqual(expected, actual)

    def test_trigram(self):
        expected = {"NNP NNP <s>": 1, "NNP NNP NNP": 1, ", NNP NNP": 1,
                "CD , NNP": 1, "RB CD ,": 1, "VBG RB CD": 1, "NN VBG RB": 1,
                ". NN VBG": 1}

        with mock.patch(self._open_name, self._mock, create=True):
            actual = datautil.get_tag_n_gram(n=3, filename="")

        self.assertEqual(expected, actual)

    def test_lemmatize_observation(self):
        lines = """
            RB women
            VBG increasing"""

        m = testsetup.mock_open()
        expected_calls = [mock.call().write("RB woman"),
                mock.call().write("\n"), mock.call().write("VBG increasing"),
                mock.call().write("\n")]

        with mock.patch(self._open_name, m, create=True):
            datautil.lemmatize_observations(lines.split("\n"), "mockoutput")

        self.assertEqual(expected_calls, m.mock_calls[2: -1])

