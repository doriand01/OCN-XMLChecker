from django.shortcuts import render
from django.http import HttpResponse
from .models import UserFile, Errors
import md5
# Create your views here.

def index(request):
	return render(request, 'xmlchecker/index.html')
def check(request):
	obj = UserFile.objects.create(xml_text=str(request.POST.items()[2][1]))
	obj.save()
	print obj
	print Errors.objects.all()
	query_to_list = list(Errors.objects.all())
	for item in Errors.objects.all():
		if (str(item) == str((obj))):
			match_err = Errors.objects.all()[query_to_list.index(item)]
	return HttpResponse('Errors: %s' % (match_err.errors))