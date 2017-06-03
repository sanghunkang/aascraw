def locate_element(elem, xpath):
	tag_parent = xpath.split("/", 1)[0]
	xpath_descendent = xpath.split("/", 1)[1]
	print(tag_parent.split(":")[0])
	print(tag_parent.split(":")[1])
	print(xpath_descendent)
	print(elem)
	elem = elem.find_all(tag_parent.split(":")[0])[int(tag_parent.split(":")[1])]
	if xpath_descendent == "PATHEND":
		print(elem.text)
		# return "DONE"
	else:
		# elem = soup.find_all(tag_parent.split(":")[0])[int(tag_parent.split(":")[1])]
		
		# print(type(doc.text))
		print('++++++++++++++++ ELSE TRIGGERED +++++++++++')
		locate_element(elem, xpath_descendent)

