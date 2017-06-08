#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import built-in packages
import os, re, sys, time
from urllib import request

# Import external packages
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np

# Import custom modules
from driverController.actions_driver import create_driver, break_into_iframe, kill_phantomjs, has_iframe, some_action
from driverController.locate_element import get_attr_elem, locate_element
from pageProcessor.codec_tag import make_seq_xpath_encoded, encode_xpath_2d, make_tsr_slice, get_seq_index_canddt
from pageProcessor.generate_xpathlist import get_HTMLdoc, get_list_xpath
from struct_detector_intra.nameyet import get_range_xpath

# Import package-wide constants
from const_global import *

#############################################################################
# url = "http://v.media.daum.net/v/20170604064504680?rcmd=r"
url = "https://www.booking.com/searchresults.html?label=gen173nr-1FCAEoggJCAlhYSDNiBW5vcmVmaH2IAQGYATHCAQN4MTHIAQzYAQHoAQH4AQKSAgF5qAID;sid=a5c024e1699d328fed4aef6c2b4495e9;checkin=2017-06-07;checkout=2017-06-08;city=-73635;from_idr=1;index_postcard=1&;ilp=1;lp_index_textlink2srdaterec=1;d_dcp=1"
doc = get_HTMLdoc(url)
soup = BeautifulSoup(doc, "html.parser")

seq_xpath = get_list_xpath(soup, [])
print(len(seq_xpath))

# seq_tag_uniq = get_seq_tag_uniq(seq_xpath)
range_xpath = get_range_xpath(seq_xpath)
# range_tag = get_range_tag(seq_tag_uniq)

# seq_pairdistmap = make_seq_pairdistmap(seq_subseq, seq_tag_uniq, shape_tsr)
# for pairdistmap in seq_pairdistmap:
# 	if abs(pairdistmap[1]) < 2:
# 		print(pairdistmap)
shape_matrix = (len(seq_xpath), range_xpath)
print(shape_matrix)
seq_xpath_encoded = make_seq_xpath_encoded(seq_xpath, shape_matrix)


# plt.imshow(seq_xpath_encoded)
# plt.axes().set_aspect('auto', 'datalim')
# plt.show()

print("#############################################################################")

depth_eval = -1
seq_index_canddt = get_seq_index_canddt(seq_xpath_encoded, depth_eval)
print("#############################################################################")

size_slice = 4
for i, index_canddt0 in enumerate(seq_index_canddt):
	tsr0 = make_tsr_slice(seq_xpath_encoded, index_canddt0, size_slice)

	for j, index_canddt1 in enumerate(seq_index_canddt[i+1:]):
		tsr1 = make_tsr_slice(seq_xpath_encoded, index_canddt1, size_slice)

		diff = tsr0 - tsr1
		dist = np.sum(diff**2)
		print(index_canddt0, index_canddt1, dist)

# for xpath in get_list_xpath(soup, []):
# 	print(xpath)
# 	# elems_located = locate_element(soup, xpath, get_attr_elem)
# 	print(elems_located[-1].attrs)


# print('++++++++++++++++++++++++++++++++++++++++')
# outputs = some_action(url)
# for output in outputs:
# 	soup = BeautifulSoup(output, "html.parser")
# 	for xpath in get_list_xpath(soup, ["p", "script"]):
# 		if "h3" in xpath:
# 			print(xpath)
# 		print(xpath)
# 	print('++++++++++++++++++++++++++++++++++++++++')