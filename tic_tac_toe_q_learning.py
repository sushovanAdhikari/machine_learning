import numpy as np
import random

'''
1 for X
-1 for Y
1 and -1 are used to switch between user
'''
class TicTacToe:
    def __init__(self, board_size = 3, computer_play = True) -> None:
        self.board_size = board_size
        self.board = np.zeros((board_size, board_size), dtype = int)
        self.current_player = 1
        self.curr_player_is_computer = False
        self.players = {
            1: 'X',
            -1: 'Y',
            # 'X': 1,
            # 'Y': -1
        }
        self.computer_play = computer_play
        self.game_over = False

    # return array of row,col for empty spots.
    def get_moves(self):
        # loop board, find the indexes where the values are 0's
        board = np.argwhere(self.board == 0)
        return board

    def is_valid_move(self, row, column):
        return 0 <= row < self.board_size and 0 <= column < self.board_size and self.board[row][column] == 0
    
    def make_move(self, row, column):
        if self.is_valid_move(row, column):
            self.board[row][column] = self.current_player
            return True
        else:
            return False
        
    def switch_player(self):
        self.current_player *= -1
        self.curr_player_is_computer  = not self.curr_player_is_computer

    def computer_move(self):
        while True:
            row = random.randint(0, self.board_size - 1)
            col = random.randint(0, self.board_size - 1)
            if self.board[row][col] == 0:
                return (row,col)
        
    def check_win(self):
        for i in range(self.board_size):
            if np.abs(self.board[i].sum()) == self.board_size or np.abs(self.board[:, i].sum()) == self.board_size:
                return True
        if np.abs(self.board.trace()) == self.board_size or np.abs(np.fliplr(self.board).trace()) == self.board_size:
            return True
        return False
    
    def check_draw(self):
        return len(np.where(self.board == 0)[0]) == 0
    
    def print_board(self):
        symbols = {1: 'X', -1: 'O', 0: ' '}
        for row in self.board:
            print(" | ".join(symbols[cell] for cell in row))
            print("-" * (self.board_size * 4 - 1))


    def get_input(self):
        if self.computer_play:
            if self.curr_player_is_computer is False:
                row, column = map(int, input(f"Player {self.players[self.current_player]}'s turn. Enter row and column (0-{self.board_size - 1}): ").split())
            else:
                row, column = self.computer_move()
        else:
            row, column = map(int, input(f"Player {self.players[self.current_player]}'s turn. Enter row and column (0-{self.board_size - 1}): ").split())
        return (row, column)
        

    def start_game(self):
        print(f"Let's play Tic-Tac-Toe on a {self.board_size}x{self.board_size} board!")
        self.print_board()

        while not self.game_over:
            while True:
                try:
                    row, column = self.get_input()
                    if self.make_move(row, column):
                        break
                    else:
                        print("Invalid move. Try again.")
                except ValueError:
                    print("Invalid input. Please enter two integers.")

            self.print_board()

            if self.check_win():
                print(f"Player {self.players[self.current_player]} wins!")
                self.game_over = True
            elif self.check_draw():
                print("It's a draw!")
                self.game_over = True
            self.switch_player()


# tic_tac_toe = TicTacToe(computer_play=False)
# tic_tac_toe.start_game()


class TrainTicTacToe(TicTacToe):
    
    def __init__(self):
        # super().__init__()
        self.x_states = {}
        self.o_states = {}
        self.track_win_count = {
            'X': 0,
            'Y': 0,
            'D': 0
        }
        ...

    def exploit(self, chance):
        threshold = 0.6
        exploit = None
        if chance >= threshold:
            exploit = False
        else: 
            exploit = True
        return exploit

    # implement q-learning exploitation and exploration
    def ttt_ex_vs_oh(self):
        super().__init__()
        game = []
        play = True
        winner = None
        while play:
            game.append(self.board.copy())
            chance = round(random.random(), 2)
            if(self.exploit(chance) == True):
                player = self.players[self.current_player]
                row, col = self.find_highest_reward_move(player)
            else:
                row, col = self.random_move()
            
            if self.players[self.current_player] is 'X':
                self.board[row][col] = 1
            else:
                self.board[row][col] = -1
            win = self.check_win()
            draw = self.check_draw()
            if win:
                play = False
                if self.players[self.current_player] is 'X':
                    winner = 'X'
                else:
                    winner = 'Y'
            elif draw:
                play = False
                winner = 'D'
            # self.update_track_win_count(status)
            self.switch_player()
        game.append(self.board.copy())

        return (winner, game)
    

    # def update_track_win_count(self, status):
    #     if status == 100:
    #         if self.players[self.current_player] is 'X':
    #             self.track_win_count['X'] += 1
    #         elif self.players[self.current_player] is 'Y':
    #             self.track_win_count['Y'] += 1
    #     else:
    #         self.track_win_count['D'] += 1
        


    def find_highest_reward_move(self, player):
        '''
        Returns the board state after making the move for the provided player from current position.

        Args:
            player(str) -> X or Y

        Returns:
            board(np) -> tictactoe board with values 1 or 0, 1 for filled, 0 for empty spots
                         note for later: 1 is used to 
        '''
        if player == 'X':
            highest_reward_state = None
            highest_reward_detect = False
            moves = self.get_moves()
            for row, col in moves:
                board = self.board.copy()
                board[row][col] = 1
                str_board = str(board)
                if str_board in self.x_states:
                    reward = self.x_states[str_board]
                else:
                    reward = 0
                if highest_reward_state:
                    if reward > highest_reward_state[0]:
                        highest_reward_detect = True
                        highest_reward_state = (reward, (row, col)) 
                else:
                    highest_reward_state = (reward, board)
            if highest_reward_detect is not True:
                row, col = random.choice(moves)
                board = self.board.copy()
                board[row][col] = 1
                reward = 0
                highest_reward_state = (reward, (row, col)) 
        else:
            highest_reward_state = None
            highest_reward_detect = False
            moves = self.get_moves()
            for row, col in moves:
                board = self.board.copy()
                board[row][col] = -1
                str_board = str(board)
                if str_board in self.o_states:
                    reward = self.o_states[str_board]
                else:
                    reward = 0
                if highest_reward_state:
                    if reward > highest_reward_state[0]:
                        highest_reward_detect = True
                        highest_reward_state = (reward, (row, col)) 
                else:
                    highest_reward_state = (reward, board)
            if highest_reward_detect is not True:
                row, col = random.choice(moves)
                board = self.board.copy()
                board[row][col] = -1
                reward = 0
                highest_reward_state = (reward, (row, col))
        return highest_reward_state[1]
    
    def random_move(self):
        moves = self.get_moves()
        row, col = random.choice(moves)
        return (row, col)
    
    def reversed(self, games):
        reversed_games = games[::-1]
        return reversed_games
    
    def update_dict(self, states, game, learning_rate, discount, reward):
        n_games = self.reversed(game)
        cumulative_reward = reward
        for board in n_games:
            board_tuple = tuple(board.flatten())

            # if board is not in dictionary
            # put it in, initial reward is 0
            if (board_tuple in states) is False:
                states[board_tuple] = 0

            # update reward

            states[board_tuple] = states[board_tuple] + learning_rate * ((discount * cumulative_reward) - states[board_tuple])
            cumulative_reward = states[board_tuple]

    def run_ttt_ex_vs_oh(self, n_games = 15000):
        for i in range(n_games):
            winner, game = self.ttt_ex_vs_oh()
            if winner is 'X':
                self.update_dict(self.x_states, game, learning_rate = 1, discount = 0.9, reward = 100)
                self.update_dict(self.o_states, game, learning_rate = 1, discount = 0.9, reward = -100)
            elif winner is 'O':
                self.update_dict(self.o_states, game, learning_rate = 1, discount = 0.9, reward = 100)
                self.update_dict(self.x_states, game, learning_rate = 1, discount = 0.9, reward = -100)
            else:
                self.update_dict(self.x_states, game, learning_rate = 1, discount = 0.9, reward = -20)
                self.update_dict(self.o_states, game, learning_rate = 1, discount = 0.9, reward = -20)

    def run(self):
        self.run_ttt_ex_vs_oh()
        print(f'X-States: {len(self.x_states)}')
        print(f'O-States: {len(self.o_states)}')
        win_x = str(self.track_win_count['X'])
        print(f'win X total:{win_x}')
        # print(f'win X total:{self.track_win_count['Y']}')
        # print(f'win X total:{self.track_win_count['D']}')


train = TrainTicTacToe()
train.run()