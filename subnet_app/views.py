from django.shortcuts import render
from .utils import calculate_subnet

# Create your views here.
def index(request):
    result = None
    if request.method == 'POST':
        ip = request.POST.get('ip')
        subnet = request.POST.get('subnet')

        result = calculate_subnet(ip, subnet)

    return render(request, 'index.html', {"result": result})