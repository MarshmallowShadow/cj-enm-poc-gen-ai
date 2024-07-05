import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models

from . import storage

intro_text = """Your are a very professional document summarization specialist.
              Given a document, your task is to strictly follow the user\'s instructions.
              please always respond in Korean unless said so otherwise."""

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 0,
    "top_p": 0.95,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH:
        generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT:
        generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT:
        generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT:
        generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}


def generate(text, document):
    result = ""
    vertexai.init(project="cj-enm-poc", location="us-central1")
    model = GenerativeModel(
        "gemini-1.5-flash-001",
    )
    responses = model.generate_content(
        [intro_text, document, text],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )
    for response in responses:
        result += response.text

    return result


def vertex_generate_data(request):
    if bool(request.FILES):
        file = request.FILES['attachment']
        file.seek(0)
        document = Part.from_data(file.read(), file.content_type)
    else:
        file_info = storage.get_file_info(request.POST['fileName'])
        document = Part.from_uri(file_info['uri'], file_info['content_type'])

    text = request.POST['question']

    if text == '질문 직접 입력':
        text = request.POST['customQuestion']

    text = text.replace("[컨텐츠]", "위 문서")

    return {"result": generate(text, document)}
