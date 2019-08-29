# Test module for kernel functions

import numpy as np

from functools import reduce
import ctypes

SIZE_XPATH_SET = 4
c_kernels = ctypes.CDLL("./aascraw/c_kernels.so")

# c_kernels.rank_tuple_vicinity.argtypes = (ctypes.c_float*4, )

c_kernels.rank_tuple_vicinity.argtypes = (ctypes.c_wchar_p * SIZE_XPATH_SET, )
# c_kernels.rank_tuple_vicinity.restype = ctypes.c_float
c_kernels.rank_tuple_vicinity.restype = ctypes.c_int

arr = ctypes.c_wchar_p * SIZE_XPATH_SET
parameter_array = arr(*["array", "of", "strings", "asdasd"])


# print(c_kernels.rank_tuple_vicinity(parameter_array))
# (xpath_set, existing_records)
# rank_tuple_vicinity = c_kernels.rank_tuple_vicinity  
def rank_tuple_vicinity(xpath_set, existing_records):

    # actions = xpath_set[i]["filterer_action"]
    filterer_actions = [xpath["filterer_action"] for xpath in xpath_set]
    # print(filterer_actions)
    c_xpath_set = (ctypes.c_wchar_p * SIZE_XPATH_SET)(*filterer_actions)

    print(len(filterer_actions))
    print(c_xpath_set)
    rank = c_kernels.rank_tuple_vicinity(c_xpath_set)
    print(rank)
    return rank
