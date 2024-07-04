from django.http import JsonResponse
from django.shortcuts import render

from demo.utils import gemini, storage


# Create your views here.
def index(request):
    file_list = storage.get_file_list()
    context = {"file_list": file_list}
    return render(request, 'main/index.html', context=context)


def summarize(request):
    if request.method == 'POST':
        try:
            response = gemini.vertex_generate_data(request)

            upload_yn = request.POST['uploadYn']
            if upload_yn == "true" and bool(request.FILES):
                file_list = storage.upload_file(request.FILES['attachment'])
                response['file_list'] = file_list

            return JsonResponse(response, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({}, status=400)

