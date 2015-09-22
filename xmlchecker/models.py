from django.db import models
from datetime import datetime
import sys
import md5

reload(sys)
sys.setdefaultencoding('utf8')
# Create your models here.
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
		self.err_list = []
		self.closed = False
		if not tag_string:
			return
		try:
			opening_1, opening_2 = tag_string.find('<'), tag_string.find('>')
			closing_1, closing_2 = tag_string.find('</', opening_1 + 1), tag_string.find('>', opening_2 + 1)
			if (closing_1 == -1) and (closing_2 != -1):
				closing = tag_string.find('/>')
				if (closing == -1) and (closing_2 == -1):
					self.err_list.append(" line {0} contains an error: Improper opening / closing.".format(line_num))
			if (opening_1 == -1) or (opening_2 == -1):
				self.err_list.append(" line {0} contains an error: Improper opening / closing.".format(line_num))
			self.string_list = tag_string.replace("<", "").replace(">", "").split()
			self.element_name = self.string_list[0]
			for string in self.string_list:
				if ('=' in string):
					attr_val = string.find('"')
					if (attr_val == -1):
						self.err_list.append(
							"line {0} contains an error: element attribute \
							{1} does not have a proper value.".format(line_num, string.partition('=')))
					elif (attr_val != -1):
						if (attr_val + 1 == string.find('=')) and not \
						   (string[-1] == '"'):
							self.err_list.append(
							"line {0} contains an error: element attribute \
							{1} does not have a proper value.".format(line_num, string.partition('=')))
					elif (attr_val != -1):
						if (string.index('=') == -1):
							self.err_list.append(
							"line {0} contains an error: element attribute \
							{1} does not have a proper value.".format(line_num, string.partition('"')))

		except (ValueError, IndexError) as e:
			self.err_list.append("line {0} contains an error:{1}".format(line_num, str(e)))
	def isClosed(self):
		if not self.closed:
			self.err_list.append("line {0} contains an error: no closing tag".format(line_num))

class MapElement(XMLElement):
	def __init__(self, tag_string, line_num):
		super(MapElement, self).__init__(tag_string, line_num)
		if not tag_string:
			return
		try:
			self.string_list = tag_string.replace("<", "").replace(">", "").split()
			self.element_name = self.string_list[0]
		except (ValueError, IndexError) as e:
			self.errors.append("XMLElement map contains an error:{1}".format(self.element_name, str(e)))
		proto_string = self.string_list[1]
		if (proto_string.find('1.4.0')==-1):
			self.err_list.append("XMLElement map contains an error: Protocol attribute is incorrect, should be 1.4.0.")

class UserFile(models.Model):
	xml_text = models.TextField()
	def __init__(self, *args, **kwargs):
		super(UserFile, self).__init__(*args, **kwargs) 
		self.errors = []
		for line in self.xml_text.split('\n'):
			num = self.xml_text.split('\n').index(line) + 1
			if ('<map' in line):
				obj = MapElement(line, num)
				for item in obj.err_list:
					self.errors.append(item)
			else:
				obj = XMLElement(line, num)
				for item in obj.err_list:
					self.errors.append(item)
	def __str__(self):
		md5_obj = md5.new()
		md5_obj.update(self.xml_text.encode('utf-8'))
		hash_str = md5_obj.hexdigest()
		return hash_str 
	def __unicode__(self):
		md5_obj = md5.new()
		md5_obj.update(str(id(self)))
		hash_str = md5_obj.hexdigest()
		return unicode(hash_str.encode('utf-8'))



				



