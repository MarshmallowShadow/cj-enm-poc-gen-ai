

def vertex_generate_data(request):
    if request.POST.get('questionType') == 'question1':
        return {"result": "A Successful Response!"}
    elif request.POST.get('questionType') == 'question2':
        return {"result": "A Successful and Meaningful Response."}
    elif request.POST.get('questionType') == 'question3':
        return {"result": "A Quite Deep Response"}
    elif request.POST.get('questionType') == 'question4':
        return {"result": "A Response"}
    else:
        return {"result": "Invalid Question."}
