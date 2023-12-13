import sys
import traceback
import json

from flask import Flask, request

from ngrok.core import get_ngrok_url
from telegram.api.core import TelegramApi

app = Flask(__name__)
TOKEN = json.load(open("./config/config.json"))['tg_token']
telegram = TelegramApi(TOKEN)

@app.route("/")
def index():
    return '', 200

@app.route('/updates', methods=['POST','GET'])
def update_listener():
    if request.method == 'POST':
        req = request.get_json()
        print(req)

    return '', 200

def compare_url():
    ngrok_url = get_ngrok_url()
    ngrok_url += "/updates"
    print("ngrok: " + ngrok_url)
    webhook_url = telegram.get_webhook_info()["result"]["url"]
    print("webhook: " + webhook_url)

    if ngrok_url != webhook_url:
        print("ngrok != webhook, setting up webhook url")
        telegram.set_webhook(ngrok_url)
        return False
    else:
        print("url's are equal, starting flask")
        return True

def main():
    try:
        compare = compare_url()
        while not compare:
            compare = compare_url()
        app.run()
    except Exception:
        print (traceback.format_exc())
        sys.exit(1)

if __name__ == '__main__':    
    main()