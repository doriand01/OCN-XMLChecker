from django.shortcuts import render
from django.http import HttpResponse
from .models import UserFile, Errors
import md5
# Create your views here.

def index(request):
	return render(request, 'xmlchecker/index.html')
def check(request):
	try:
		obj = UserFile.objects.create(xml_text=str(request.POST.items()[2][1].encode('utf-8')))
		obj.save()
		hash_str = str(obj)
		err_obj = Errors.objects.create(errors='<br/>'.join(obj.errors), errors_es='<br/>'.join(obj.errors_es), _id=hash_str)
		if ('es' in request.environ['LANGUAGE']) or ('ES' in request.environ['LANGUAGE']):
			return render(request, 'xmlchecker/check.html', {"errors" : err_obj.errors_es})
		elif ('en' in request.environ['LANGUAGE']) or ('EN' in request.environ['LANGUAGE']):
			return render(request, 'xmlchecker/check.html', {"errors" : err_obj.errors})
	except IndexError:
		return render(request, 'xmlchecker/no_post_data.html')
