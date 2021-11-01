from django.shortcuts import render


# Create your views here.

def first_page(request):
    link = f"http://89.108.70.128/admin/"
    return render(request, './index.html', {'link': link})
