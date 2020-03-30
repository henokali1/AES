from django.shortcuts import render

def sp_products_all(request):
	args={}
	return render(request, 'sp_products/sp_products_all.html', args)