from django.shortcuts import render

# Create your views here.

def index(req):
    return render(req, "main/index.html")

def contact(request):
    return render(request, "main/contact.html")