# coding: utf-8
'''
Created on May 15, 2014

@author: uidv9994
'''

import sys

# DIRECTORY IMPORT AREA
sys.path.append(r'D:\Sandboxes\SW_AUT_ITS\Software\Library\Workspace\PLAST_wa\Tests')


# FILES IMPORT AREA
from TSC_ReqModule_1_2_3                            import TEST_1
from TSC_ReqModule_4                                import TEST_2
from TSC_ReqModule_5                                import TEST_3
from TSC_ReqModule_6                                import TEST_4
from TSC_ReqModule_7                                import TEST_5
from TSC_ReqModule_8                                import TEST_6

# add test case function here separated by a comma
listOfAllTests = [
                    TEST_1 ,
                    TEST_2 ,
                    TEST_3 ,
                    TEST_4 ,
                    TEST_5 ,
                    TEST_6 ,
                 ]