from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    context = {}
    template = "bills/index.html"
    return render(request, template, context)



