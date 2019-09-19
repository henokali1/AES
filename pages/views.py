from django.views.generic import TemplateView
from django.shortcuts import render



def pages(request):
    return render(request, 'pages/pages.html')

def cat_urls(request, cat_urls):
	urls = str(request.get_full_path())
	urls = urls[22:]
	sp = urls.split(',')
	
	for i in sp:
		print("------------------------------------------------------------------------------")
		print(i)

	args={'cats':cat_urls}
	return render(request, 'pages/cats.html', args)