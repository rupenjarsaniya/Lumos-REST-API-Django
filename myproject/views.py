from django.http import HttpResponse, JsonResponse


def index(request):
    return HttpResponse("Hello, world. Django App is working...")

def ping(request):
    return HttpResponse("pong🏓")

def version(request):
    return JsonResponse({"version": "1.0.0", "status": "ok"})