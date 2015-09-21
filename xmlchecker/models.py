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
	def __init__(self, tag_string, line_num):
		self.closed = False
		if not tag_string:
			return
		try:
			opening_1, opening_2 = tag_string.find('<'), tag_string.find('>')
			closing_1, closing_2 = tag_string.find('</', opening_1 + 1), tag_string.find('>', opening_2 + 1)
			if closing_1 == -1:
				closing = tag_string.find('/>')
			if (opening_1 == -1) or (opening_2 == -1):
				err_list.append("XMLElement at line {0} contains an error: Improper opening".format(line_num))
			self.string_list = tag_string.replace("<", "").replace(">", "").split()
			self.element_name = self.string_list[0]
		except (ValueError, IndexError) as e:
			err_list.append("XMLElement {0} contains an error:{1}".format(self.element_name, str(e)))
	def isClosed(self):
		if not self.closed:
			err_list.append("XMLElement {0} contains an error: no closing tag")

class MapElement(XMLElement):
	def __init__(self, tag_string, line_num):
		super(MapElement, self).__init__(tag_string, line_num)
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
		found_error_object = False
		for line in self.xml_text.split('\n'):
			num = self.xml_text.split('\n').index(line) + 1
			if ('<map' in line):
				obj = MapElement(line, num)
			else:
				obj = XMLElement(line, num)
		md5_obj = md5.new()
		md5_obj.update(self.xml_text)
		hash_str = md5_obj.hexdigest() 
		query_to_list = list(Errors.objects.all())
		if query_to_list:
			for item in query_to_list:
				if str(item) == hash_str:
					found_error_object = True
					return hash_str + 'old'
				if not found_error_object:
					err_obj = Errors(errors='\n'.join(err_list), _id=hash_str)
					err_obj.save()
		else:
			err_obj = Errors(errors='\n'.join(err_list), _id=hash_str)
			err_obj.save()
			return hash_str
	def __unicode__(self):
		found_error_object = False
		md5_obj = md5.new()
		md5_obj.update(self.xml_text.encode('utf-8'))
		hash_str = md5_obj.hexdigest() 
		query_to_list = list(Errors.objects.all())
		for item in query_to_list:
			if str(item) == hash_str:
				found_error_object = True
				return hash_str + 'old'
			if not found_error_object:
				err_obj = Errors(errors='\n'.join(err_list), _id=hash_str)
				err_obj.save()
		return hash_str
		md5_obj = md5.new()
		md5_obj.update(str(id(self)))
		hash_str = md5_obj.hexdigest()
		return unicode(hash_str.encode('utf-8'))



				



