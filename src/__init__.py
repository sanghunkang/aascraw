#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import built-in packages
import os, re, sys, time
from urllib import request

# Import 3rd-party packages
# import requests # do I need this?
from bs4 import BeautifulSoup

# Import custom modules
from actions_driver import create_driver, break_into_iframe, kill_phantomjs, has_iframe
from generate_xpathlist import get_HTMLdoc, get_list_xpath
from locate_element import locate_element

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

testlist = []

url = "http://v.media.daum.net/v/20170604064504680?rcmd=r"
doc = get_HTMLdoc(url)
soup = BeautifulSoup(doc, "html.parser")

print('++++++++++++++++++++++++++++++++++++++++')
get_list_xpath(soup, ["script","p"])
# for xpath in get_list_xpath(soup, ["script","p"]):
# 	# print(xpath)
# 	if "h3" in xpath:
# 		elem_located = locate_element(soup, xpath)
# 		print(elem_located)

# 		for attr in elem_located.attrs:
# 			print(attr)

# outputs = some_action(url)
# for output in outputs:
# 	soup = BeautifulSoup(output, "html.parser")
# 	for xpath in get_list_xpath(soup):
# 		if "h3" in xpath:
# 			print(xpath)
# 			testlist.append(xpath)
# 		# print(xpath)
# 	print('++++++++++++++++++++++++++++++++++++++++')
