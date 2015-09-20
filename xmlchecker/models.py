from django.db import models
import md5
from datetime import datetime

# Create your models here.
err_list = []
class Errors(models.Model):
	errors = models.TextField()
	_id = models.CharField(max_length=100)
	def __str__(self):
		return self._id
	def __unicode__(self):
		return unicode(self._id)
class XMLElement(object):
	def close(self):
		self.closed = True
	def __init__(self, tag_string, *args, **kwargs):
		self.closed = False
		if not tag_string:
			return
		try:
			self.string_list = tag_string.replace("<", "").replace(">", "").split()
			self.element_name = self.string_list[0]
		except (ValueError, IndexError) as e:
			self.errors.append("XMLElement {0} contains an error:{1}".format(self.element_name, str(e)))
	def isClosed(self):
		if not self.closed:
			err_list.append("XMLElement {0} contains an error: no closing tag")

class MapElement(XMLElement):
	def __init__(self, tag_string, *args, **kwargs):
		self.closed = False
		if not tag_string:
			return
		try:
			self.string_list = tag_string.replace("<", "").replace(">", "").split()
			print self.string_list
			self.element_name = self.string_list[0]
		except (ValueError, IndexError) as e:
			self.errors.append("XMLElement map contains an error:{1}".format(self.element_name, str(e)))
		proto_string = self.string_list[1]
		print proto_string
		if (proto_string.find('1.4.0')==-1):
			err_list.append("XMLElement map contains an error: Protocol attribute is incorrect, should be 1.4.0.")

class UserFile(models.Model):
	xml_text = models.TextField() 
	def __str__(self):
		for line in self.xml_text.split('\n'):
			if ('<map' in line):
				obj = MapElement(line)
			else:
				obj = XMLElement(line)
		md5_obj = md5.new()
		md5_obj.update(self.xml_text)
		hash_str = md5_obj.hexdigest() 
		err_obj = Errors(errors='\n'.join(err_list), _id=hash_str)
		err_obj.save()
		return hash_str
	def __unicode__(self):
		md5_obj = md5.new()
		md5_obj.update(str(id(self)))
		hash_str = md5_obj.hexdigest()
		return unicode(hash_str)



				



