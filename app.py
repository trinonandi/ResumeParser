import json
from io import BytesIO

from flask import Flask, request, Response
from flask_cors import CORS, cross_origin

from pdf_utils import extract_text_from_pdf, convert_to_html
from llm_utils import get_response_from_query

app = Flask(__name__)
cors = CORS(app)


@app.route('/')
@cross_origin()
def hello_world():  # put application's code here
    return "hello world!"


# TODO: Cap file upload limit
@app.post('/upload')
@cross_origin()
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
    markdown_string = convert_to_html(json.loads(extracted_json))
    response = Response(markdown_string)
    response.status_code = 200
    response.headers["Content-Type"] = "text/plain"

    return response


@app.post('/chat')
@cross_origin()
def chat():
    body = request.json

    api_key = body.get("apiKey")
    context = body.get("context")
    query = body.get("query")

    if not api_key or not context or not query:
        return "Bad Request", 400

    answer = get_response_from_query(context, query, api_key)
    response = Response(answer)
    response.status_code = 200
    response.headers["Content-Type"] = "text/plain"

    return response, 200


if __name__ == '__main__':
    app.run()
