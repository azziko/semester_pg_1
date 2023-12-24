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

class Matchmaker:
    def __init__(self):
        self.players_waiting = []
    
    def join_matchmaking(self, player):
        self.players_waiting.append(player)
        self.match_players()

    def match_players(self):
        if len(self.players_waiting) >= 2:
            player1, player2 = self.players_waiting[:2]
            self.players_waiting = self.players_waiting[2:]

            player1.opponent = player2
            player2.opponent = player1

            self.notify_match(player1, player2)

    def leave_matchmaking(self, player):
        if player in self.players_waiting:
            self.players_waiting.remove(player)

    def notify_match(self, player1, player2):
        pass

    def disconnect_players(self, player):
        if player.opponent:
            self.notify_disconnect(player.opponent)
            player.opponent.opponent = None
            player.opponent = None

    def notify_disconnect(self, player):
        pass


def determine_winner(player1, player2):
    if player1 == player2:
        return 'It\'s a tie!'

    if win_combs[player1] == player2:
        return 'Player 1 wins!'

    return 'Player 2 wins!'

def generate_random_choice():
    options = ['🪨', '✂️', '📃']
    return random.choice(options)