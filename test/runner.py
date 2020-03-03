import unittest
from .test_enroll import EnrollTest
from .test_authenticate import AuthenticateTest

loader = unittest.TestLoader()
test_suite = unittest.TestSuite()

test_suite.addTest(loader.loadTestsFromTestCase(EnrollTest))
test_suite.addTest(loader.loadTestsFromTestCase(AuthenticateTest))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(test_suite)