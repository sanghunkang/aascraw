#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import built-in packages
import os, re, sys, time
from urllib import request

# Import 3rd-party packages
# import requests # do I need this?
from bs4 import BeautifulSoup

# Import custom modules
from locate_element import locate_element
from actions_driver import create_driver, break_into_iframe, kill_phantomjs, has_iframe
from generate_xpathlist import get_HTMLdoc, get_list_xpath

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

url = "http://v.media.daum.net/v/20170602205505233"
doc = get_HTMLdoc(url)
soup = BeautifulSoup(doc, "html.parser")
print('++++++++++++++++++++++++++++++++++++++++')
for xpath in get_list_xpath(soup):
	print(xpath)
	testlist.append(xpath)


# outputs = some_action(url)
# for output in outputs:
# 	soup = BeautifulSoup(output, "html.parser")
# 	for xpath in get_list_xpath(soup):
# 		if "h3" in xpath:
# 			print(xpath)
# 			testlist.append(xpath)
# 		# print(xpath)
# 	print('++++++++++++++++++++++++++++++++++++++++')

print('++++++++++++++++++++++++++++++++++++++++')
elem = BeautifulSoup(doc, "html.parser")
xpath = "html:0/body:0/div:1/div:2/div:0/div:0/h3:0/PATHEND"
locate_element(elem, xpath)
