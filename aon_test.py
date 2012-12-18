import unittest
from aon import parse_string

test_str = 'Welcome to \r\nMandriva Linux release 2007.0 (Official) for x86_64\r\nKernel 2.6.22 on a Dual-processor x86_64\r\n    NCEN=VELTON/12-12-05/16 H 57 IDENTIFICATION OF MALICIOUS CALLS\r\r\n          ND-DE = 577177736           NE-DE = 001-10-127\r\r\n          ND-DR =   952357487        AFCT-DR = 222-038-08\r\r\n\r\n'
test_str2 = '    NCEN=VELTON/12-12-05/16 H 59 IDENTIFICATION OF MALICIOUS CALLS\r\r\n          ND-DE = 577174414           NE-DE = 007-06-114\r\r\n          ND-DR =   577177751        NE-DR = 001-11-023\r\r\n\r\n'


class TestAon(unittest.TestCase):
    """ TestCase for AON app. """
    def test_parsing(self):
        """
        Test for correct input value to str_parsing.
        """
        self.assertEqual(parse_string(test_str, '577177736'),
                                     '0952357487 12-12-05 16:57')
        self.assertEqual(parse_string(test_str, '577177737'), None)
        self.assertEqual(parse_string(test_str2, '577174414'),
                                     '0577177751 12-12-05 16:59')
        self.assertEqual(parse_string(test_str2, '577174415'), None)
        self.assertRaises(TypeError, parse_string, test_str, 999)
        self.assertRaises(TypeError, parse_string, 999, 999)
        self.assertRaises(ValueError, parse_string, '', '577174415')
        self.assertRaises(ValueError, parse_string, test_str, '')
        self.assertRaises(ValueError, parse_string, '', '')
        self.assertRaises(ValueError, parse_string, test_str, ' ')


suite = unittest.TestLoader().loadTestsFromTestCase(TestAon)
unittest.TextTestRunner(verbosity=2).run(suite)
