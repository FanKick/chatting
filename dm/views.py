from django.shortcuts import render

# Create your views here.
def dm_page(request):
    return render(request, 'dm/dm_page.html')