import requests

headers = {
    'sec-ch-ua-platform': '"macOS"',
    'Referer': 'https://www.geoguessr.com/game/RglsByjJEYDKQtfu',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'Content-Type': 'application/json',
    'sec-ch-ua-mobile': '?0',
    'X-Client': 'web',
}

json_data = {
    'token': 'RglsByjJEYDKQtfu',
    'lat': 25.200693117092683,
    'lng': 55.299004750109745,
    'timedOut': False,
    'stepsCount': 4,
}

response = requests.post('https://www.geoguessr.com/api/v3/games/RglsByjJEYDKQtfu', headers=headers, json=json_data)

print(response)