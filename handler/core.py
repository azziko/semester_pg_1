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
            player = mm.get_player(chat_id)
            if player == None:
                player = game.Player(chat_id)
                mm.players_db(player)

            if player.opponent != None:
                return self.client.send_message(chat_id, 'Already matched!')

            joined = mm.join_matchmaking(player)

            if joined != None:
                text = 'Opponent found, make a choice'
                self.client.send_message(joined.chat_id, text)
                self.client.send_message(joined.opponent.chat_id, text)

                self.client.send_options(joined.chat_id)
                self.client.send_options(joined.opponent.chat_id)
            else: 
                self.client.send_message(chat_id, 'Waiting for the worthy opponent')
                self.client.send_options(chat_id)
        
        if text.startswith('Close'):
            player = mm.get_player(chat_id)
            if player != None:
                mm.leave_matchmaking(player)
                player_id, opponent_id = mm.disconnect_players(player)
                if opponent_id != -1:
                    self.client.delete_options(player_id, 'You were disconnected')
                    self.client.delete_options(opponent_id, 'Your opponents left the match')
                else: 
                    self.client.delete_options(player_id, 'Closed')
            else: 
                self.client.delete_options(player_id, 'Closed')

        return '', 200