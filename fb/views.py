from django.shortcuts import render
from .models import *


# Create your views here.
def interests(request):
    fb_interests = FbInterest.objects.all().order_by('-audience_size')
    args = {'fb_interests': fb_interests}
    return render(request, 'fb/interests.html', args)