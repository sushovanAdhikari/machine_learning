import numpy as np
from random import randrange, random

# initialize q-table
q_table = np.empty((0, 2))

# initialize game setup
board_reward_values = np.array([-100,0,0,0,0,0,0,0,0,0,100,0]) 

# initialize q-movement-matrix
q_movement_matrix = np.array(
        [[0,1],
        [0,2],
        [1,3],
        [2,4],
        [3,5],
        [4,6],
        [5,7],
        [6,8],
        [7,9],
        [8,10],
        [9,11],
        [10,11]]
    )  

for state, value in enumerate(board_reward_values):
        state_action = np.array([0,0])
        q_table = np.vstack([q_table,state_action])

def select_random_action(available_actions):
    random_number = np.random.choice(available_actions)
    return random_number

def q_learning_game(player_state, reward_state, pit_state):
        threshold = 0.5
        playing = True

        while (playing):
            chance = round(random(), 2)

            if chance > threshold:
                action = select_random_action(len(q_table[0]))
            else:
                # Get the index(action) of the highest value in the specified row
                # note: q_table column values represents the action
                action = np.argmax(max(q_table[player_state]))

            next_state = q_movement_matrix[player_state, action]
            q_table[player_state, action] = board_reward_values[next_state] + max(q_table[next_state])
            player_state = next_state

            if player_state == pit_state:
                print('oopps fell into a pit. Try again!')
                break

            if player_state == reward_state:
                print('Eating Cheese')
                break
        
        print(q_table)

q_learning_game(3,10,0)