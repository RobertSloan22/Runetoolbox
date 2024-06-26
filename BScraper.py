import requests
from bs4 import BeautifulSoup

def scrape_text(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        text = ' '.join(p.get_text() for p in soup.find_all('p'))
        return text
    except Exception as e:
        return f"Error: {e}"

# Example URL
url = ""
data = scrape_text(url)
print(data)
