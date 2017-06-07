#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import built-in packages
import os, re, sys, time
from urllib import request

# Import external packages
from bs4 import BeautifulSoup

# Import custom modules
from actions_driver import create_driver, break_into_iframe, kill_phantomjs, has_iframe
from generate_xpathlist import get_HTMLdoc, get_list_xpath
from locate_element import get_attr_elem, locate_element
from struct_detector_intra.nameyet import calculate_similarity, define_dim, get_depth_max, matrixify_xpath, subsample_seq_xpath, tensify_sumsample

#############################################################################
# Define constants
SYSTEM = sys.platform
PATH_DRIVER = os.path.abspath('..') + '/drivers/'

def some_action(url):
	driver = create_driver(SYSTEM, PATH_DRIVER)	
	driver.get(url)
	outputs = []
	
	iframes = driver.find_elements_by_tag_name('iframe')
	for iframe in iframes:
		outputs.append(break_into_iframe(driver, iframe))
	
	kill_phantomjs(driver)		
	return outputs

url = "http://v.media.daum.net/v/20170604064504680?rcmd=r"
# url = "https://www.booking.com/searchresults.html?label=gen173nr-1FCAEoggJCAlhYSDNiBW5vcmVmaH2IAQGYATHCAQN4MTHIAQzYAQHoAQH4AQKSAgF5qAID;sid=a5c024e1699d328fed4aef6c2b4495e9;checkin=2017-06-07;checkout=2017-06-08;city=-73635;from_idr=1;index_postcard=1&;ilp=1;lp_index_textlink2srdaterec=1;d_dcp=1"
doc = get_HTMLdoc(url)
soup = BeautifulSoup(doc, "html.parser")

print(len(get_list_xpath(soup, [])))
seq_xpath = get_list_xpath(soup, [])
vec_index = define_dim(seq_xpath)
depth = get_depth_max(seq_xpath)

size_sumsample = 4
seq_subsample = subsample_seq_xpath(seq_xpath, size_sumsample)

import numpy as np
tsr_0 = np.zeros(shape=(size_sumsample, depth, len(vec_index)))

for subsample in seq_subsample:
	tsr_1 = tensify_sumsample(subsample, depth, vec_index)
	aa = calculate_similarity(tsr_0, tsr_1)
	tsr_0 = tsr_1
	
	print(aa)
	if abs(aa) < 2:
		for xpath in subsample:
			print(xpath)

	print("+++++++++++++++++++++++++++++++++")
	# print(tsr)
	# for xpath in subsample:
	# 	print(xpath)
	# 	bb = matrixify_xpath(xpath, depth, vec_index)
	# 	print(bb)

# for xpath in get_list_xpath(soup, []):
# 	print("   ")
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
