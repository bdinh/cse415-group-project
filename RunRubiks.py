'''
Bao Dinh, Andrew Kan, Chris Oh
CSE 415
Project
'''

import MDP
import board
import numpy as np
import ast

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.patches import Polygon

facedict = ["U", "D", "F", "B", "R", "L"]


def test():
    global facedict

    board.createInitialCube()
    # Currently initial state is a np array
    initial_state = board.initial_board

    cube_MDP = MDP.MDP()
    cube_MDP.register_start_state(initial_state)
    cube_MDP.register_winning_state(board.WINNING_STATE)
    cube_MDP.register_actions(board.ACTIONS)
    cube_MDP.register_operators(board.OPERATORS)
    cube_MDP.register_transition_function(board.T)
    cube_MDP.register_reward_function(board.R)

    cube_MDP.generateAllStatesWithHeuristics()
    # cube_MDP.generateAllStates()
    # print(str(cube_MDP.winning_state) in cube_MDP.known_states)
    # print(len(cube_MDP.known_states))
    # print(len(cube_MDP.succArray))

    # s = str(cube_MDP.winning_state)
    # path = []
    # actions = []
    # while s != -1:
    #     path.append(s)
    #     stateAction = cube_MDP.backlink[s]
    #     s = stateAction[1]
    #     a = stateAction[0]
    #     actions.append(a)
    #
    # path.reverse()
    # actions.reverse()
    # # print(path)
    # # print(actions)
    #
    # initial_state_array = np.array(initial_state).tolist()
    #
    # print("Initial State")
    # for i in range(len(initial_state_array)):
    #     print(facedict[i] + " " + str(initial_state_array[i]))
    # print("\n")
    #
    #
    # print(printCube(path, actions))





    cube_MDP.valueIteration(.9, 10)

    # cube_MDP.QLearning(0.9, 2, 0.5)

    # print(cube_MDP.QValues)
    # print(cube_MDP.extractBestMove())



def printCube(path, action):
    global facedict
    result = ""
    for n in range(len(path)):
        if n == len(path) - 1:
            currentAction = "Solved State"
        else:
            currentAction = action[n + 1]
        board = ast.literal_eval(path[n])
        # print(board[0])
        result += "Action " + str(n) + ":  Best Action: " + currentAction + "\n"
        for i in range(len(board)):
            result += facedict[i] + " " + str(board[i]) + "\n"
        result += "\n"
    return result



def render(self, flat=True, views=True):
    """
    Visualize the cube in a standard layout, including a flat,
    unwrapped view and three perspective views.
    """
    assert flat or views
    xlim = (-2.4, 3.4)
    ylim = (-1.2, 4.)
    if not flat:
        ylim = (2., 4.)
    if not views:
        xlim = (-1.2, 3.2)
        ylim = (-1.2, 2.2)
    fig = plt.figure(figsize=((xlim[1] - xlim[0]) * self.N / 5., (ylim[1] - ylim[0]) * self.N / 5.))
    ax = fig.add_axes((0, 0, 1, 1), frameon=False,
                      xticks=[], yticks=[])
    if views:
        self.render_views(ax)
    if flat:
        self.render_flat(ax)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    return fig

def render_flat(self, ax):
    """
    Make an unwrapped, flat view of the cube for the `render()`
    function.  This is a map, not a view really.  It does not
    properly render the plastic and stickers.
    """
    for f, i in self.facedict.items():
        x0, y0 = self.pltpos[i]
        cs = 1. / self.N
        for j in range(self.N):
            for k in range(self.N):
                ax.add_artist(Rectangle((x0 + j * cs, y0 + k * cs), cs, cs, ec=self.plasticcolor,
                                        fc=self.stickercolors[self.stickers[i, j, k]]))
        ax.text(x0 + 0.5, y0 + 0.5, f, color=self.labelcolor,
                ha="center", va="center", rotation=20, fontsize=self.fontsize)
    return None


test()

