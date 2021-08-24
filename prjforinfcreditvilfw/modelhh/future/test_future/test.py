
'''
Created on Dec 11, 2017

@author: fan
'''
import unittest

if __name__ == '__main__':
    testsuite = unittest.TestLoader().discover('.')
    unittest.TextTestRunner(verbosity=1).run(testsuite)
