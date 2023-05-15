import requests
from PyPDF2 import PdfReader
from io import BytesIO
import re
import json



def remove_markdown_and_html(text):
    # Remove markdown links
    text = re.sub(r'\[.*?\]\(.*?\)', '', text)
    # Remove html tags
    text = re.sub(r'<.*?>', '', text)
    return text

def pdf_to_text_and_upsert(url):
    response = requests.get(url)
    pdf = PdfReader(BytesIO(response.content))
    text = ''
    for page in range(len(pdf.pages)):
        text += pdf.pages[page].extract_text()
    text = remove_markdown_and_html(text)
    # Upsert to vector db
    upsert_url = 'https://unaidedelf8777-expert-umbrella-5wgj4g5ppq6hv6px-8000.preview.app.github.dev/upsert'
    headers = {'Content-Type': 'application/json'}
    data = {'documents': [
        {'text': text}]}
    response = requests.post(upsert_url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print('Text successfully upserted to vector db.')
    else:
        print('Failed to upsert text to vector db.')

pdf_url = 'https://arxiv.org/pdf/2305.04790.pdf'
pdf_to_text_and_upsert(pdf_url)


def upload_from_pdf_url(pdf_url):
    pdf_to_text_and_upsert(pdf_url)

