import random

win_combs = {
    'rock': 'scissors',
    'scissors': 'paper',
    'paper': 'rock',
}

class Player:
    def __init__(self, chat_id):
        self.id = chat_id
        self.opponent = None
        self.choice = None

class Matchmaker:
    def __init__(self):
        self.players_db = []
        self.players_waiting = []
    
    def join_matchmaking(self, player):
        if player not in self.players_waiting and player.opponent is None:
            self.players_waiting.append(player)
            return self.match_players()   

        return None 

    def match_players(self):
        if len(self.players_waiting) >= 2:
            player1, player2 = self.players_waiting[:2]
            self.players_waiting = self.players_waiting[2:]

            player1.opponent = player2
            player2.opponent = player1

            return player1

        return None

    def leave_matchmaking(self, player):
        if player in self.players_waiting:
            self.players_waiting.remove(player)

    def disconnect_players(self, player):
        '''
        Disconnects player and its opponent 
        returning ids of both or -1, -1 otherwise.
        '''

        opponent_id = -1
        player_id = -1
        if player.opponent != None:
            opponent_id = player.opponent.chat_id
            player_id = player.chat_id

            player.opponent.opponent = None
            player.opponent = None

        return player_id, opponent_id

    def get_player(self, chat_id):
        '''
        Searches player by id in db and returns one if exists
        None otherwise
        '''

        for player in self.players_db:
            if player.id == chat_id:
                return player
        return None

def determine_winner(player1, player2):
    if player1 == player2:
        return 'It\'s a tie!'

    if win_combs[player1] == player2:
        return 'Player 1 wins!'

    return 'Player 2 wins!'

def generate_random_choice():
    options = ['🪨', '✂️', '📃']
    return random.choice(options)