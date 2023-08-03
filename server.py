import flask
import json
import os
from flask import request
from core.quiz_converter import QuizConverter

app = flask.Flask(__name__)


@app.post('/api/quiz2quiz')
def quiz2quiz():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == None:
        return 'No file selected'

    # only accept docx
    if file.filename.split('.')[-1] != 'docx':
        return 'File extension not allowed'

    # convert docx to JSON
    quiz_converter = QuizConverter(file)
    json_data = quiz_converter.get_json()

    path = f'data/{quiz_converter.id}'
    if not os.path.exists(path):
        os.makedirs(path)

    with open(f'data/{quiz_converter.id}/questions.json', 'w', encoding='utf8') as f:
        json_questions = {
            'questions': []
        }

        for count, question in enumerate(json_data['questions']):

            json_questions['questions'].append({
                'number': count,
                'content': question['content'],
                'choices': question['choices']
            })

        json.dump(json_questions, f, ensure_ascii=False)

    with open(f'data/{quiz_converter.id}/answers.json', 'w', encoding='utf8') as f:
        json_answers = {
            'answers': []
        }

        for count, question in enumerate(json_data['questions']):
            json_answers['answers'].append({
                'number': count,
                'answer': question['answer']
            })

        json.dump(json_answers, f, ensure_ascii=False)

    return {
        'testid': quiz_converter.id,
        'num_questions': len(json_data['questions'])
    }


@app.get('/data/<id>/questions')
def questions(id):
    return flask.send_from_directory(f'data/{id}', 'questions.json')


@app.get('/data/<id>/answers')
def answers(id):
    return flask.send_from_directory(f'data/{id}', 'answers.json')


@app.get('/data/<id>/media/<filename>')
def media(id, filename):
    return flask.send_from_directory(f'data/{id}/word/media', filename)


app.run(port=8000, debug=True)
