from django.shortcuts import render

from .utils import calculate_subnet


def index(request):
    result = None
    ip_value = ""
    subnet_value = ""
    if request.method == "POST":
        ip_value = request.POST.get("ip") or ""
        subnet_value = request.POST.get("subnet") or ""
        result = calculate_subnet(ip_value, subnet_value)

    return render(
        request,
        "index.html",
        {
            "result": result,
            "ip_value": ip_value,
            "subnet_value": subnet_value,
        },
    )
