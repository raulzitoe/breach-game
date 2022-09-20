import string
import random

class GameManager:
    def __init__(self, redis_client):
        self.redis_client = redis_client
        if not self.redis_client.exists("breach:games_count"):
            self.redis_client.set("breach:games_count", 0)

    def create_game(self):
        new_game_id = int(self.redis_client.get("breach:games_count")) + 1
        self.redis_client.set("breach:games_count", new_game_id)
        board = self.generate_random_board(new_game_id)

        # Create token for joining the game
        token = self.generate_random_token()
        self.redis_client.hset("breach:token", token, new_game_id)

        self.redis_client.hset("breach:game_status", new_game_id, "started;waiting_player2")
        game_state = {
            'game_id': new_game_id,
            'token': token,
        }
        game_state.update(board)
        return game_state

    def generate_random_board(self, game_id):
        # generate and store board, with player positions
        self.redis_client.hset("breach:player1_pos", game_id, 0)
        self.redis_client.hset("breach:player2_pos", game_id, 0)

        return {
            'player1_pos': 0,
            'player2_pos': 0,
        }

    def get_board(self, game_id):
        return {
            'game_id': game_id,
            'player1_pos': int(self.redis_client.hget("breach:player1_pos", game_id)),
            'player2_pos': int(self.redis_client.hget("breach:player2_pos", game_id)),
        }

    def join_game(self, token):
        if self.redis_client.hexists("breach:token", token):
            # consume token
            game_id = int(self.redis_client.hget("breach:token", token))
            self.redis_client.hdel("breach:token", token)
            return self.get_board(game_id)

        return {}
    
    def move_left(self, game_id, player):
        if self.redis_client.hexists(f"breach:{player}_pos", game_id):
            current_pos = int(self.redis_client.hget(f"breach:{player}_pos", game_id))
            new_pos = current_pos - 1
            self.redis_client.hset(f"breach:{player}_pos", game_id, new_pos)
            return new_pos
        return -1 # should return error instead

    def move_right(self, game_id, player):
        if self.redis_client.hexists(f"breach:{player}_pos", game_id):
            current_pos = int(self.redis_client.hget(f"breach:{player}_pos", game_id))
            new_pos = current_pos + 1
            self.redis_client.hset(f"breach:{player}_pos", game_id, new_pos)
            return new_pos
        return -1 # should return error instead

    def generate_random_token(self, length=16):
        # from https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits/23728630#23728630
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))