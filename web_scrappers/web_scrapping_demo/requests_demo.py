import requests

def get_web_page(url):
    response = requests.get(url)
    return response.content.decode('utf-8')


 

 