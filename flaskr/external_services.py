import os

import requests


def upload_image(file):
    api_key = os.getenv('IMAGE_UPLOAD_API_KEY')
    api_url = os.getenv('IMAGE_UPLOAD_API_URL')
    return requests.post(api_url, data=dict(key=api_key), files=dict(source=file))


