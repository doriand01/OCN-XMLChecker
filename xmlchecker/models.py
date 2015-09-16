from django.db import models

# Create your models here.

class UserFile(models.Model):
	xml_text=models.TextField()

class XMLElement(object):
	def close(self):
		self.closed = True
	def __init__(self, tag_string):
		self.closed = False
		self.errors = []
		try:
		    self.string_list = tag_string.replace("<", "").replace(">", "").split()
		    self.element_name = self.string_list[0]
		except ValueError as e:
			self.errors.append("XMLElement {0} contains an error:{1}".format(self.element_name, str(e)))
			return "XMLElement contains an error:" + str(e)
	def isClosed(self):
		if not self.closed:
			self.errors.append("XMLElement {0} contains an error: no closing tag")


class MapXML(object):
	def __init__(self, xml):


