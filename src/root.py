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
<<<<<<< HEAD
from locate_element import locate_element
from struct_detector_intra import nameyet
=======
from locate_element import get_attr_elem, locate_element
>>>>>>> slave

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


<<<<<<< HEAD
seq_tag = []
for descnt in soup.descendants:
	seq_tag.append(descnt.name)

print(len(seq_tag))
set_tag = set(seq_tag)
print(set_tag)
dict_tag = {}
for i, tag in enumerate(set_tag):
	dict_tag[tag] = i#seq_tag.count(tag)
	print(tag, dict_tag[tag])

# SORT?
seq_tag_y = [dict_tag[tag] for tag in seq_tag]
print(seq_tag_y)

import matplotlib.pyplot as plt
plt.plot(set_tag, seq_tag_y)
plt.show()
# get_list_xpath(soup, ["p", "script"])
# for xpath in get_list_xpath(soup, ["script","p"]):
# 	# print(xpath)
# 	if "p" in xpath:
# 		elem_located = locate_element(soup, xpath)
# 		print(elem_located)

# 		for attr in elem_located.attrs:
# 			print(attr)
=======
print(len(get_list_xpath(soup, [])))
for xpath in get_list_xpath(soup, [])[-20:]:
	print("   ")
	print(xpath)
	elem_located = locate_element(soup, xpath, get_attr_elem)
	print(elem_located[-1].attrs)
>>>>>>> slave

# print('++++++++++++++++++++++++++++++++++++++++')
# outputs = some_action(url)
# for output in outputs:
# 	soup = BeautifulSoup(output, "html.parser")
# 	for xpath in get_list_xpath(soup, ["p", "script"]):
# 		if "h3" in xpath:
# 			print(xpath)
# 		print(xpath)
# 	print('++++++++++++++++++++++++++++++++++++++++')
