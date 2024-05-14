from io import BytesIO

from flask import Flask, request

from pdf_utils import extract_text_from_pdf
from llm_utils import create_vector_db, get_response_from_query

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.post('/upload')
def upload_pdf():
    if 'pdfFile' not in request.files:
        return 'No file found', 400

    file = request.files['pdfFile']

    if file.filename == '':
        return 'No selected file', 400

    if file:
        file_content = file.read()
        pdf_file = BytesIO(file_content)
        text = extract_text_from_pdf(pdf_file)
        db = create_vector_db(text)
        response = get_response_from_query(db, "Generate a cover letter out of the resume")
        print(response)

    return 'File successfully uploaded', 200


if __name__ == '__main__':
    app.run()
