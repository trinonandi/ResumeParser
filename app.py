import json
from io import BytesIO

from flask import Flask, request

from pdf_utils import extract_text_from_pdf

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.post('/upload')
def upload_pdf():
    if 'pdfFile' not in request.files:
        return json.dumps({"Error": "File not found"}), 400

    file = request.files['pdfFile']
    if not file:
        return json.dumps({"Error": "File not found"}), 400

    if file.filename == '':
        return json.dumps({"Error": "No selected file"}), 400

    file_content = file.read()
    pdf_file = BytesIO(file_content)
    extracted_json = extract_text_from_pdf(pdf_file)
    # text = extract_text_from_pdf(pdf_file)
    # db = create_vector_db(text)
    # response = get_response_from_query(db, "Generate a cover letter out of the resume")
    # print(json)
    return extracted_json, 200


if __name__ == '__main__':
    app.run()
