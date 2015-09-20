from django.shortcuts import render
from django.http import HttpResponse
from .models import UserFile, Errors
import md5
# Create your views here.

def index(request):
	return render(request, 'xmlchecker/index.html')
def check(request):
	obj = UserFile.objects.create(xml_text=str(request.POST.items()[2][1].encode('utf-8')))
	obj.save()
	print obj
	query_to_list = list(Errors.objects.all())
	hash_str = str(obj)
	try:
		if hash_str.endswith('old'):
			hash_str = hash_str.replace('old', '')
			print 'old item.'
			for item in Errors.objects.all():
				if str(item) == str(hash_str):
					match_err = Errors.objects.all()[query_to_list.index(item)]
			return HttpResponse('Errors: %s' % (match_err.errors))
		for item in Errors.objects.all():
			if (str(item) == str((obj))):
				match_err = Errors.objects.all()[query_to_list.index(item)]
		return HttpResponse('Errors: %s' % (match_err.errors))
	except Exception as e:
		print str(e)
		return HttpResponse('Errors: Error object could not be found.')