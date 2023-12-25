import random

win_combs = {
    'rock': 'scissors',
    'scissors': 'paper',
    'paper': 'rock',
}

class Player:
    def __init__(self, chat_id):
        self.id = chat_id
        self.opponent = False
        self.choice = None

class Matchmaker:
    def __init__(self):
        self.players_pool = []
    
    def join_matchmaking(self, player):
        # change it such that if player is not already playing, return none and not append
        # And if already searching return none and not append
        if player not in self.players_pool and player.opponent is None:
            self.players_pool.append(player)
            return self.match_players()   

        return None 

    def match_players(self):
        if len(self.players_pool) >= 2:
            player1, player2 = self.players_pool[:2]
            self.players_pool = self.players_pool[2:]

            player1.opponent = player2
            player2.opponent = player1

            return player1

        return None

    def leave_matchmaking(self, player):
        if player in self.players_pool:
            self.players_pool.remove(player)

    def disconnect_players(self, player):
        if player.opponent:
            self.notify_disconnect(player.opponent)
            player.opponent.opponent = None
            player.opponent = None

    def notify_disconnect(self, player):
        pass

    def get_player(self, chat_id):
        for player in self.players_waiting:
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