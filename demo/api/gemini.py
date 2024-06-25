import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models


intro_text = ("""Your are a very professional document summarization specialist."""
              """Given a document, your task is to strictly follow the user\'s instructions.""")

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
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
    text = ''
    if request.POST.get('questionType') == 'question1':
        text = """Please summarize the above document in korean."""
    elif request.POST.get('questionType') == 'question2':
        text = """Please summarize the above document in japanese."""
    elif request.POST.get('questionType') == 'question3':
        text = """Please summarize the above document in german."""
    elif request.POST.get('questionType') == 'question4':
        text = """Please summarize the above document in English."""
    else:
        return {"result": "Invalid Question."}

    document = Part.from_uri(
        mime_type="application/pdf",
        uri="gs://cloud-samples-data/generative-ai/pdf/fdic_board_meeting.pdf")

    return {"result": generate(text, document)}
