from django.http import JsonResponse
from django.shortcuts import render


# Create your views here.
def index(request):

    return render(request, 'main/index.html')


def summarize(request):
    if request.method == 'POST':
        return JsonResponse({"result": "A Successful Response!"}, status=200)
    else:
        return JsonResponse({}, status=400)

