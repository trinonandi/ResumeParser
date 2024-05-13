from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.post('/upload')
def upload_pdf():
    if 'pdfFile' not in request.files:
        return 'No file found', 404

    file = request.files['pdfFile']

    if file.filename == '':
        return 'No selected file', 404

    return 'File successfully uploaded', 200


if __name__ == '__main__':
    app.run()
