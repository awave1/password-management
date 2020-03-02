import unittest
from enroll_test import EnrollTest
from authenticate_test import AuthenticateTest

loader = unittest.TestLoader()
test_suite = unittest.TestSuite()

test_suite.addTest(loader.loadTestsFromTestCase(EnrollTest))
test_suite.addTest(loader.loadTestsFromTestCase(AuthenticateTest))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(test_suite)
