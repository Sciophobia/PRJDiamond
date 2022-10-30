# Project: Project Diamond, Application Five Unit Test
# Purpose Details: Tests functionality of Application Five's methods.
# Course: IST 411
# Author: Sciophobia (Timothy)
# Date Developed: 10/31/2021
# Last Date Changed: 10/31/2021
# Rev: 1
import unittest

from APP5 import App5


class MyTestCase(unittest.TestCase):

    def test_log(self):
        print("***test_log***")
        A5 = App5
        self.assertEqual(A5.log(A5, "Unit Test", "Testing logging connection"), {'nodeName': "Unit Test", 'activityDescription': "Testing logging connection"})

    if __name__ == '__main__':
        unittest.main()
