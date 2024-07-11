import base64
from decimal import Decimal

import vertexai
from vertexai.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models

from . import storage

intro_text = """Users are now movie or drama producers who are looking for new IP content to find success.
                To do this, we want to know all the details about the content you specify.
                Your job is to accurately and faithfully follow the user's instructions and respond in detail.
                Unless otherwise stated, please always respond in Korean."""

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


def generate(text, document, temperature, top_p, presence_penalty):
    result = ""
    vertexai.init(project="cj-enm-poc", location="asia-northeast3")
    model = GenerativeModel(
        "gemini-1.5-flash-001",
    )

    generation_config = {
        "max_output_tokens": 8192,
        "temperature": temperature,
        "top_p": top_p,
        "presence_penalty": presence_penalty,
    }

    responses = model.generate_content(
        [intro_text, document, text],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )
    for response in responses:
        result += response.text

    return result


# Vertex AI 호출 전 로직 (변수 선언)
def vertex_generate_data(request):
    if bool(request.FILES):
        file = request.FILES['attachment']
        file.seek(0)
        document = Part.from_data(file.read(), file.content_type)
    else:
        file_info = storage.get_file_info(request.POST['fileName'])
        document = Part.from_uri(file_info['uri'], file_info['content_type'])

    temperature = Decimal(request.POST['temperature'])
    top_p = Decimal(request.POST['topP'])
    presence_penalty = Decimal(request.POST['presencePenalty'])

    text = request.POST['question']
    if text == '질문 직접 입력':
        text = request.POST['customQuestion']

    return generate(text, document, temperature, top_p, presence_penalty)
