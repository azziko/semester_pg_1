class Handler:
    def __init__(self, client):
        self.client = client

    def route(self, req):
        chat_id = req['message']['chat']['id']
        text = req['message']['text']
        
        if text.startswith('/start'):
            print(text)
    
        if text.startswith('/play_bot'):
            print(text)
            self.client.send_options(chat_id)

        if text.startswith('/play_online'):
            print(text)
        
        return '', 200