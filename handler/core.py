import logic.core as game

mm = game.Matchmaker() 

class Handler:
    def __init__(self, client):
        self.client = client

    def route(self, req):
        chat_id = req['message']['chat']['id']
        text = req['message']['text']

        if text.startswith('/start'):
            self.client.send_message(chat_id, 
                'Welcome! Try your luck with other players /play_online or challenge the bot /play_bot'
            )
    
        if text.startswith('/play_bot'):
            self.client.send_message(chat_id, 'Try your luck, warrior!')
            self.client.send_options(chat_id)

        if text.startswith('/play_online'):
            # do not create a player if already playing
            player = game.Player(chat_id)
            joined = mm.join_matchmaking(player)

            if joined != None:
                text = 'Opponent found, make a choice'
                self.client.send_message(joined.chat_id, text)
                self.client.send_message(joined.opponent.chat_id, text)

                self.client.send_options(joined.chat_id)
                self.client.send_options(joined.opponent.chat_id)
            else: 
                self.client.send_message(chat_id, 'Waiting for the worthy opponent')
        
        if text.startswith('Close'):
            self.client.delete_options(chat_id, 'Closed')

        return '', 200