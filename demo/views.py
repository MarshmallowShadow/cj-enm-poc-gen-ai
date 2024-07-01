from django.http import JsonResponse
from django.shortcuts import render

from demo.utils import gemini


# Create your views here.
def index(request):
    return render(request, 'main/index.html')


def summarize(request):
    if request.method == 'POST':
        try:
            response = gemini.vertex_generate_data(request)
            return JsonResponse(response, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({}, status=400)

