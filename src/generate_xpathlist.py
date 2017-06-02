# Import built-in packages
import os, re, sys, time

from urllib import request

# Import 3rd-party packages
import requests

from bs4 import BeautifulSoup
from selenium import webdriver

# Define constants
SYSTEM = sys.platform
print(SYSTEM)

def get_HTMLdoc(url):
	req = request.urlopen(url)
	charset = req.info().get_content_charset()
	ret = req.read().decode(charset)
	return ret

def get_list_xpath(doc, path_prev="", ret=[]):
	list_tmp = []
	for child in doc.children:
		i = list_tmp.count(child.name)
		list_tmp.append(child.name)

		if hasattr(child, 'children') == True and len(list(child.children)) <= 1:			
			ret.append(path_prev.lstrip("/") + "/"+ child.name + "[{0}]".format(i))
		elif hasattr(child, 'children') == True:
			get_list_xpath(child, path_prev + "/"+ child.name + "[{0}]".format(i), ret)
	
	return ret

def create_driver_phantomjs(system):
	if "linux" in system:
		path_phantomjs = "./phantomjs"
	elif "win" in system:
		path_phantomjs = ".\\phantomjs.exe"
	ret = webdriver.PhantomJS(path_phantomjs)
	return ret

def create_driver(system, type_driver="phantomjs"):
	if type_driver == "phantomjs":
		ret = create_driver_phantomjs(system)
	return ret

def kill_phantomjs(driver):
	driver.close()
	driver.quit()

def break_into_iframe(driver, iframe):
	driver.switch_to_frame(iframe)
	ret = driver.page_source
	driver.switch_to_default_content()
	return ret

def defined_driver():
	pass

def has_iframe(url):
	driver = create_driver(SYSTEM)	
	driver.get(url)
	try:
		driver.find_element_by_tag_name('iframe')
	except selenium.common.exceptions.NoSuchElementException:
		ret = False
	else:
		ret = True
	return ret



def some_action(url):
	driver = create_driver(SYSTEM)	
	driver.get(url)
	outputs = []
	
	iframes = driver.find_elements_by_tag_name('iframe')
	for iframe in iframes:
		outputs.append(break_into_iframe(driver, iframe))
	
	kill_phantomjs(driver)		
	return outputs




url = "http://cafe.naver.com/firenze/4747507"
doc = get_HTMLdoc(url)
soup = BeautifulSoup(doc, 'html.parser')

print('++++++++++++++++++++++++++++++++++++++++')

outputs = some_action(url)
for output in outputs:
	soup = BeautifulSoup(output, "html.parser")
	for xpath in get_list_xpath(soup):
		print(xpath)
	print('++++++++++++++++++++++++++++++++++++++++')