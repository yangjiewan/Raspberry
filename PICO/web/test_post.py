import json
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
}
data = json.dumps({"id": 4, "method": "test", "params": ["11111"]})
url = "http://127.0.0.1/reset"
response = requests.post(url=url, data=data, headers=headers)
