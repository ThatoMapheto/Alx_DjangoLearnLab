from django.http import HttpResponse


def home(request):
    return HttpResponse("Relationship App is working!")
