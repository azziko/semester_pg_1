import requests
import json

class TelegramApi(object):
    URL = "https://api.telegram.org/bot"

    def __init__(self, token):
        self.token = token

    def send_message(self, chat_id, text, mode_html=False):
        _url = self.URL + self.token + "/sendMessage"
        if mode_html:
            data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
        else:
            data = {"chat_id": chat_id, "text": text}
        req = requests.post(_url, json=data)

        return req.json()
    
    def send_options(self, chat_id):
        _url = self.URL + self.token + "/sendMessage"
        keyboard = [
            ['🪨', '✂️', '📃'],
            ['Close']
        ]
        reply_markup = {'keyboard': keyboard, 'resize_keyboard': True, 'one_time_keyboard': False}

        data = {
            'chat_id': chat_id,
            'text': 'Choose an option:',
            'reply_markup': reply_markup,
        }
        req = requests.post(_url, json=data)

        return req.json()
    
    def delete_options(self, chat_id, text):
        _url = self.URL + self.token + "/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': text,
            'reply_markup': json.dumps({'remove_keyboard': True})
        }
        req = requests.post(_url, json=data)

        return print(req.json())

    def set_webhook(self, url):
        _url = self.URL + self.token + "/setWebhook"
        data = {"url": url}
        req = requests.post(_url, json=data)
        req.raise_for_status()

        return req.json()

    def get_webhook_info(self):
        _url = self.URL + self.token + "/getWebhookInfo"
        req = requests.get(_url)
        req.raise_for_status()

        return req.json()

    def delete_webhook(self):
        _url = self.URL + self.token + "/deleteWebhook"
        req = requests.get(_url)

        return req.json()
