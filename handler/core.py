import logic.core as game

mm = game.Matchmaker() 

class Handler:
    def __init__(self, client):
        self.client = client

    def route(self, req):
        '''process request according to message received'''

        chat_id = req['message']['chat']['id']
        text = req['message']['text']

        if text.startswith('/start'):
            player = mm.get_player(chat_id)
            if player == None:
                player = game.Player(chat_id)
                mm.players_db.append(player)
            
            self.client.send_message(chat_id, 
                'Welcome! Try your luck with other players /play_online or challenge the bot /play_bot'
            )
    
        if text.startswith('/play_bot'):
            self.client.send_message(chat_id, 'Try your luck, warrior!')
            self.client.send_options(chat_id)

        if text.startswith('/play_online'):
            player = mm.get_player(chat_id)

            #Create player in case first command sent is not start
            if player == None:
                player = game.Player(chat_id)
                mm.players_db.append(player)

            if player.opponent != None:
                return self.client.send_message(chat_id, 'Already matched!')

            joined = mm.join_matchmaking(player)

            if joined != None:
                text = 'Opponent found, make a choice'
                self.client.send_message(joined.id, text)
                self.client.send_message(joined.opponent.id, text)

                self.client.send_options(joined.id)
                self.client.send_options(joined.opponent.id)
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

        if text in ['🪨', '✂️', '📃']:
            player = mm.get_player(chat_id)
            if player.opponent != None:
                if player.opponent.choice != None:
                    winner = game.determine_winner(text, player.opponent.choice)
                    match winner:
                        case 0:
                            self.client.send_message(
                                chat_id, f'{text} on {player.opponent.choice}. It\'s a draw!'
                            )
                            self.client.send_message(
                                player.opponent.id, f'{player.opponent.choice} on {text}. It\'s a draw!'
                            )
                        case 1:
                            self.client.send_message(
                                chat_id, f'{text} on {player.opponent.choice}. You won!'
                            )
                            self.client.send_message(
                                player.opponent.id, f'{player.opponent.choice} on {text}. You lost!'
                            )
                        case 2:
                            self.client.send_message(
                                chat_id, f'{text} on {player.opponent.choice}. You lost!'
                            )
                            self.client.send_message(
                                player.opponent.id, f'{player.opponent.choice} on {text}. You won!'
                            )
                    player.opponent.choice = None
                else: 
                    player.choice = text
                    self.client.send_message(chat_id, 'The choice was made! Wait for your opponent to respond')
            else:
                bot_choice = game.generate_random_choice() 
                winner = game.determine_winner(text, bot_choice)
                response = f'{text} on {bot_choice}'

                match winner:
                    case 0:
                        self.client.send_message(chat_id, f'{response}. It\'s a draw against the bot!')
                    case 1:
                        self.client.send_message(chat_id, f'{response}. You won the bot!')
                    case 2:
                        self.client.send_message(chat_id, f'{response}. The bot won!')

        return '', 200