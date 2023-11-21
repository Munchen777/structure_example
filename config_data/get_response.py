import requests


def get_response(url, headers):
    return requests.get(url, headers=headers)
