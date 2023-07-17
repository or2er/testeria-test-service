import flask
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
    return quiz_converter.get_json()


@app.get('/media/<id>/<filename>')
def media(id, filename):
    return flask.send_from_directory(f'data/{id}/word/media', filename)


app.run(port=8000, debug=True)
