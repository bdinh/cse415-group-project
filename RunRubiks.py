import MDP
import board
import numpy as np

def test():

    board.createInitialCube()
    # Currently initial state is a np array
    initial_state = board.initial_board
    print(initial_state)
    cube_MDP = MDP.MDP()
    cube_MDP.register_start_state(initial_state)
    cube_MDP.register_winning_state(board.WINNING_STATE)
    cube_MDP.register_actions(board.ACTIONS)
    cube_MDP.register_operators(board.OPERATORS)
    cube_MDP.register_transition_function(board.T)
    cube_MDP.register_reward_function(board.R)


    # cube_MDP.state_neighbors(initial_state)
    # print(cube_MDP.known_states)
    # print(cube_MDP.succArray)
    cube_MDP.generateAllStates()
    print(len(cube_MDP.succArray))
    test = []
    print(len(cube_MDP.known_states))






    # print(cube_MDP.succArray)
    # print(cube_MDP.known_states)

    # cube_MDP.register_start_state()



test()