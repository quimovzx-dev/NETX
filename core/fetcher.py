import requests
from config import REQUEST_TIMEOUT, USER_AGENT

def fetch(url):
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.text
