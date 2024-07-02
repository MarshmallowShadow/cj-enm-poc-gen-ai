from django.http import JsonResponse
from django.shortcuts import render

from demo.utils import gemini, storage


# Create your views here.
def index(request):
    return render(request, 'main/index.html')


def summarize(request):
    if request.method == 'POST':
        try:
            file = request.FILES['attachment']
            question_type = request.POST['questionType']
            upload_yn = request.POST['uploadYn']

            if upload_yn == "true":
                storage.upload_file(file)

            response = gemini.vertex_generate_data(file, question_type)

            return JsonResponse(response, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({}, status=400)

