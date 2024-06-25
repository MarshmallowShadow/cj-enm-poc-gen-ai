from django.http import JsonResponse
from django.shortcuts import render

from demo.api import gemini


# Create your views here.
def index(request):

    return render(request, 'main/index.html')


def summarize(request):
    if request.method == 'POST':
        response = gemini.vertex_generate_data(request)
        return JsonResponse(response, status=200)

    else:
        return JsonResponse({}, status=400)

