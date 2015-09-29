# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
from .defined import defined_elements
import sys
import md5
valid_opening_vals = [str([True, True, False, True, True]), str([True, True, True, False, False]),
str([True, True, False, False, False]), str([True, False, True, False, False])]
reload(sys)
sys.setdefaultencoding('utf8')
# Create your models here.
class Errors(models.Model):
	errors = models.TextField()
	errors_es = models.TextField()
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
		self.err_list_es = []
		self.closed = False
		self.err_string = "line {0} contains an error: ".format(line_num)
		self.err_string_es = "la línea {0} contiene un error:".format(line_num)
		tag_string = tag_string.replace('\n', ' ').replace('\r', ' ')
		if (tag_string.find('<!') != -1):
			tag_string = tag_string.partition('<!')[0]
			if len(tag_string.partition('<!')) != 3:
				return
		if not tag_string:
			return
		opening_1, opening_2, opening_3 = tag_string.find('<'), tag_string.find('>'), tag_string.find('/>')
		closing_1, closing_2, = tag_string.find('</', opening_1 + 1), tag_string.find('>', opening_2 + 1)
		tag_opening_values = [opening_1, opening_2, opening_3, closing_1, closing_2]
		for item in tag_opening_values:
			if (item == -1):
				tag_opening_values[tag_opening_values.index(item)] = False
			else:
				tag_opening_values[tag_opening_values.index(item)] = True
		if str(tag_opening_values) not in valid_opening_vals:
			self.err_list.append(self.err_string + 'Improper opening/closing value.')
			self.err_list_es.append(self.err_string_es + 'Apertura inadecuado o valor de cierre.')
			return
		repls = {'<' : ' ', '</' : ' ', '>' : ' ', '/>' : ' '}
		self.string_list = reduce(lambda a, kv: a.replace(*kv), repls.iteritems(), tag_string).split()
		self.element_name = self.string_list[0]
		if self.element_name not in defined_elements:
			self.err_list.append(self.err_string + 'Element <{0}> is not defined in docs.oc.tc '.format(line_num))
			self.err_list_es.append(self.err_string_es + 'Elemento <{0}> no está definido en docs.oc.tc')

	def isClosed(self):
		if not self.closed:
			self.err_list.append("line {0} contains an error: no closing tag".format(line_num))
class MapElement(XMLElement):
	def __init__(self, tag_string, line_num):
		super(MapElement, self).__init__(tag_string, line_num)
		if not tag_string:
			return
		try:
			self.string_list = tag_string.replace("<", " ").replace(">", " ").split()
			self.element_name = self.string_list[0]
		except (ValueError, IndexError) as e:
			self.errors.append("XMLElement map contains an error:{1}".format(self.element_name, str(e)))
		proto_string = self.string_list[1]
		if (proto_string.find('1.4.0')==-1):
			self.err_list.append("XMLElement map contains an error: Protocol attribute is incorrect, should be 1.4.0.")
			self.err_list_es.append("XMLElement 'mapa' contiene un error: atributo Protocolo es incorrecto, debe ser 1.4.0.")

class UserFile(models.Model):
	xml_text = models.TextField()
	def __init__(self, *args, **kwargs):
		super(UserFile, self).__init__(*args, **kwargs)
		self.errors = []
		self.errors_es = []
		for line in self.xml_text.split('\n'):
			num = self.xml_text.split('\n').index(line) + 1
			if ('<map' in line):
				obj = MapElement(line, num)
				for item in obj.err_list:
					self.errors.append(item)
				for item in obj.err_list_es:
					self.errors_es.append(item)
			else:
				obj = XMLElement(line, num)
				for item in obj.err_list:
					self.errors.append(item)
				for item in obj.err_list_es:
					self.errors_es.append(item)
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
