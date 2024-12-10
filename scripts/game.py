import requests
from bs4 import BeautifulSoup

headers = {
    'sec-ch-ua-platform': '"macOS"',
    'Referer': 'https://www.geoguessr.com/game/F1QrowbzHd8a3JFN',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'X-Client': 'web',
}

response = requests.get('https://www.geoguessr.com/game/F1QrowbzHd8a3JFN', headers=headers)
soup = BeautifulSoup(response.text,'html.parser')

print(soup)