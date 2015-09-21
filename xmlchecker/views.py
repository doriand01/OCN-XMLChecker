from django.shortcuts import render
from django.http import HttpResponse
from .models import UserFile, Errors
import md5
# Create your views here.

def index(request):
	return render(request, 'xmlchecker/index.html')
def check(request):
        print request.POST.items()
	obj = UserFile.objects.create(xml_text=str(request.POST.items()[2][1].encode('utf-8')))
	obj.save()
	hash_str = str(obj)
	err_obj = Errors.objects.create(errors='\n'.join(obj.errors), _id=hash_str)
	return HttpResponse('Errors:' + err_obj.errors)
