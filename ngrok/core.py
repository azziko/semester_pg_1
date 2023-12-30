import re
import json

import requests

def get_ngrok_url():
    req = requests.get("http://127.0.0.1:4040/api/tunnels")
    
    req = req.json()
    return req['tunnels'][0]['public_url']