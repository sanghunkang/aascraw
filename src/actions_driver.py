#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import 3rd-party packages
import selenium
from selenium import webdriver

def defined_driver():
	pass

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

def has_iframe(driver, url):
	driver = create_driver(SYSTEM)
	driver.get(url)
	try:
		driver.find_element_by_tag_name('iframe')
	except selenium.common.exceptions.NoSuchElementException:
		ret = False
	else:
		ret = True
	return ret

def break_into_iframe(driver, iframe):
	driver.switch_to_frame(iframe)
	ret = driver.page_source
	driver.switch_to_default_content()
	return ret

def kill_phantomjs(driver):
	driver.close()
	driver.quit()