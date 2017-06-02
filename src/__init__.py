#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import built-in packages
import os, re, sys, time
from urllib import request

# Import 3rd-party packages
# import requests # do I need this?
from bs4 import BeautifulSoup

# Import custom modules
import locate_element
from actions_driver import create_driver, break_into_iframe, kill_phantomjs, has_iframe
from generate_xpathlist import get_HTMLdoc, get_list_xpath

#############################################################################
# Define constants
SYSTEM = sys.platform
print(SYSTEM)


# def defined_driver():
# 	pass

def some_action(url):
	driver = create_driver(SYSTEM)	
	driver.get(url)
	outputs = []
	
	iframes = driver.find_elements_by_tag_name('iframe')
	for iframe in iframes:
		outputs.append(break_into_iframe(driver, iframe))
	
	kill_phantomjs(driver)		
	return outputs

url = "http://v.media.daum.net/v/20170602205505233"
doc = get_HTMLdoc(url)
soup = BeautifulSoup(doc, "html.parser")
print('++++++++++++++++++++++++++++++++++++++++')

outputs = some_action(url)
for output in outputs:
	soup = BeautifulSoup(output, "html.parser")
	for xpath in get_list_xpath(soup):
		print(xpath)
	print('++++++++++++++++++++++++++++++++++++++++')