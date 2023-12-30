import random

win_combs = {
    '🪨': '✂️',
    '✂️': '📃',
    '📃': '🪨',
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
        '''
        Adds player to the queue and invokes match_player function
        '''

        if player not in self.players_waiting and player.opponent is None:
            self.players_waiting.append(player)
            return self.match_players()   

        return None 

    def match_players(self):
        '''
        If there are >2 players in the waiting queue, match the first two
        and remove them from the queue, returning the player
        who was first to join the queue, None otherwise.
        '''

        if len(self.players_waiting) >= 2:
            player1, player2 = self.players_waiting[:2]
            self.players_waiting = self.players_waiting[2:]

            player1.opponent = player2
            player2.opponent = player1

            return player1

        return None

    def leave_matchmaking(self, player):
        '''Disconnects a player from the matchmaking if present'''

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
            opponent_id = player.opponent.id
            player_id = player.id

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
    '''
    Determines winner of two choices. 
    Returns 0 on draw, 1 on player1 win and 2 on player2 win.
    '''

    if player1 == player2:
        return 0

    if win_combs[player1] == player2:
        return 1

    return 2

def generate_random_choice():
    options = ['🪨', '✂️', '📃']
    return random.choice(options)