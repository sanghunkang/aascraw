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
from interInspector import get_unqseq_xpath_encoded, get_intersect_xpath_encoded, make_map, shrink_seq_xpath_encoded
from pageProcessor.codecTag import make_seq_xpath_encoded, encode_xpath_2d, make_tsr_slice, get_seq_index_canddt, update_seq_index_canddt, calculate_dist_tsr
from pageProcessor.generate_xpathlist import XpathFinder, get_range_xpath, get_HTMLdoc

# Import package-wide constants
from constGlobal import *

#############################################################################
url1 = "https://www.tripadvisor.co.kr/Attraction_Review-g294217-d2482919-Reviews-or30-Hong_Kong_Skyline-Hong_Kong.html"
url2 = "https://www.tripadvisor.co.kr/Attraction_Review-g294217-d2482919-Reviews-or40-Hong_Kong_Skyline-Hong_Kong.html"
# url = "https://www.amazon.com/s/ref=br_pdt_mgUpt/136-5748595-7690834?_encoding=UTF8&rh=n%3A1055398&srs=10112675011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=&pf_rd_r=H0CVS4CGFH8ZKDF3N54G&pf_rd_t=36701&pf_rd_p=db21a8d3-3560-4f95-b840-a0a07adc52e0&pf_rd_i=desktop"
# url = "http://v.media.daum.net/v/20170609204506833?rcmd=r"
# url = "http://movie.naver.com/movie/bi/mi/basic.nhn?code=155256"
# url = "http://movie.naver.com/movie/bi/mi/basic.nhn?code=156083"

# sampl1
url = url1
doc = get_HTMLdoc(url)
soup = BeautifulSoup(doc, "html.parser")
xpathFinder = XpathFinder()
seq_xpath = xpathFinder.make_seq_xpath(soup)

range_xpath = get_range_xpath(seq_xpath)
shape_matrix = (len(seq_xpath), range_xpath)
# seq_xpath_encoded = make_seq_xpath_encoded(seq_xpath, shape_matrix)
seq_xpath_encoded_0 = make_seq_xpath_encoded(seq_xpath, shape_matrix)
print(seq_xpath_encoded_0.shape)

# # sampl2
url = url2
doc = get_HTMLdoc(url)
soup = BeautifulSoup(doc, "html.parser")
xpathFinder = XpathFinder()
seq_xpath = xpathFinder.make_seq_xpath(soup)
range_xpath = get_range_xpath(seq_xpath)

shape_matrix = (len(seq_xpath), range_xpath)
seq_xpath_encoded_1 = make_seq_xpath_encoded(seq_xpath, shape_matrix)
print(seq_xpath_encoded_1.shape)
print("#############################################################################")

unqseq_xpath_encoded_0 = get_unqseq_xpath_encoded(seq_xpath_encoded_0)
print(unqseq_xpath_encoded_0.shape)
unqseq_xpath_encoded_1 = get_unqseq_xpath_encoded(seq_xpath_encoded_1)
print(unqseq_xpath_encoded_1.shape)
print("#############################################################################")

intersect_xpath_encoded = get_intersect_xpath_encoded(unqseq_xpath_encoded_0, unqseq_xpath_encoded_1)
print(len(intersect_xpath_encoded))	


seq_map_xpath0 = make_map(seq_xpath_encoded_0, intersect_xpath_encoded)
print(len(seq_map_xpath0))
seq_map_xpath1 = make_map(seq_xpath_encoded_1, intersect_xpath_encoded)
print(len(seq_map_xpath1))

shrunkseq_xpath_encoded_0 = shrink_seq_xpath_encoded(seq_xpath_encoded_0, seq_map_xpath0)
shrunkseq_xpath_encoded_1 = shrink_seq_xpath_encoded(seq_xpath_encoded_1, seq_map_xpath1)

if len(seq_xpath_encoded_0) < len(seq_xpath_encoded_1):
	sxe0 = seq_xpath_encoded_0
	sxe1 = seq_xpath_encoded_1
else:
	sxe0 = seq_xpath_encoded_1
	sxe1 = seq_xpath_encoded_0
print("#############################################################################")
# nicely nested
# unnicely nested
# unnested

dist = 0
i = 0
padding = 0
while i < sxe0.shape[0]:
	try:
		print(i, i + padding)
		print(sxe0[i])
		print(sxe1[i + padding])

		dist = calculate_dist_tsr(sxe0[i], sxe1[i+padding])
		print(dist)
		
		if dist == 0:
			i += 1
		else:
			padding += 1

	except IndexError: # which implies non-nested
		x = i
		break

print("#############################################################################")
i = sxe0.shape[0] -1
padding = 0
while i >= 0:
	try:
		print(i, i - padding)
		print(sxe0[i])
		print(sxe1[i - padding])

		dist = calculate_dist_tsr(sxe0[i], sxe1[i - padding])
		print(dist)
		
		if dist == 0:
			i -= 1
		else:
			padding -= 1

	except IndexError: # which implies non-nested
		y = i
		break

print(x, y)

	

# seq_xpath_encoded = make_seq_xpath_encoded(seq_xpath, shape_matrix)

# plt.imshow(seq_xpath_encoded)
# plt.axes().set_aspect('auto', 'datalim')
# plt.show()

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
# 	print("#############################################################################")
# 	print("#############################################################################")