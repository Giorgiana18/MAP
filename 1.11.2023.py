import requests
from bs4 import BeautifulSoup

def get_author_and_date(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # pentru autor
    author = soup.find('meta', {'name': 'author'})
    if author:
        author = author.get('content')

    # pentru data publicării
    date = soup.find('meta', {'name': 'date'})
    if date:
        date = date.get('content')

    # pentru titlu
    title = soup.find('title')
    if title:
        title = title.text.strip()
    return author, date, title

url = "https://ziaruldebacau.ro/ultima-ora-cnair-semneaza-cu-o-firma-din-turcia-contractul-pentru-ultimul-lot-din-autostrada-a7-moldova/"

author, date, title = get_author_and_date(url)
print(f"Autor: {author}")
print(f"Data: {date}")
print(f"Titlu: {title}")