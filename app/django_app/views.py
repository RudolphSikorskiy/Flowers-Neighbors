from django.shortcuts import render


# Create your views here.

def first_page(request):
    link = "http://localhost:8000/admin/"
    return render(request, './index.html', {'link': link})
