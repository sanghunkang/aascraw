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
from driverController.driver import webdriverTailored
from driverController.locator import get_attr_elem, locate_element
from pageProcessor.codecTag import make_seq_xpath_encoded, encode_xpath_2d, make_tsr_slice, get_seq_index_canddt, update_seq_index_canddt
from pageProcessor.generate_xpathlist import get_range_xpath, get_HTMLdoc, get_list_xpath

# Import package-wide constants
from constGlobal import *

#############################################################################
url = "https://www.tripadvisor.co.kr/Attraction_Review-g294217-d2482919-Reviews-or40-Hong_Kong_Skyline-Hong_Kong.html"
url = "https://www.amazon.com/s/ref=br_pdt_mgUpt/136-5748595-7690834?_encoding=UTF8&rh=n%3A1055398&srs=10112675011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=&pf_rd_r=H0CVS4CGFH8ZKDF3N54G&pf_rd_t=36701&pf_rd_p=db21a8d3-3560-4f95-b840-a0a07adc52e0&pf_rd_i=desktop"
url = "http://v.media.daum.net/v/20170609204506833?rcmd=r"
doc = get_HTMLdoc(url)
soup = BeautifulSoup(doc, "html.parser")

"""
driver = webdriverTailored(PATH_DRIVER)
driver.get(url)
driver.detect_seq_iframe()
for i, iframe in enumerate(driver.seq_iframe):
	psrc = driver.get_pagesource_in_iframe(i)
	soup = BeautifulSoup(psrc, "html.parser")	
	for xpath in get_list_xpath(soup,[]): #, ["p", "script"]):
		print(xpath)
	print("#############################################################################")
driver.kill()
"""

# seq_xpath = get_list_xpath(soup, [])
# range_xpath = get_range_xpath(seq_xpath)
# shape_matrix = (len(seq_xpath), range_xpath)
# print(shape_matrix)

# seq_xpath_encoded = make_seq_xpath_encoded(seq_xpath, shape_matrix)

# # plt.imshow(seq_xpath_encoded)
# # plt.axes().set_aspect('auto', 'datalim')
# # plt.show()

# depth_eval = -1
# for depth_eval in range(-1, -10, -1):
# 	seq_index_canddt = get_seq_index_canddt(seq_xpath_encoded, depth_eval)
# 	print(seq_index_canddt)

# 	for size_slice in range(1, 4):
# 		seq_index_canddt_new = update_seq_index_canddt(seq_xpath_encoded, seq_index_canddt, size_slice)
# 		seq_index_canddt = seq_index_canddt_new
# 		print(seq_index_canddt)
# 	print("#############################################################################")

# 	for index_canddt in seq_index_canddt:
# 		xpath = seq_xpath[index_canddt]
# 		elems_located = locate_element(soup, xpath, get_attr_elem)
# 		print(elems_located[-1].text)
# print("#############################################################################")
# print("#############################################################################")

# print("#############################################################################")
