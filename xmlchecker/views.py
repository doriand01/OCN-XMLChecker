from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import UserFile, Errors
import md5
# Create your views here.

def index(request):
	return render(request, 'xmlchecker/index.html')
def check(request):
	obj = UserFile.objects.create(xml_text=request.POST.items()[2][1].encode('utf-8'))
	obj.save()
	hash_str = str(obj)
	err_obj = Errors.objects.create(errors='<br/>'.join(obj.errors), _id=hash_str)
	return HttpResponse('Errors:' + err_obj.errors)
