import random
import copy
import numpy as np

class MDP:
    def __init__(self):
        self.known_states = set()  # as a string in array format
        self.succ = {} # hash of adjacency lists by state. (string: np array)
        self.succArray = {} # (string: array)

    def register_start_state(self, start_state):
        self.start_state = start_state # in np array
        self.known_states.add(str(self.nptoArray(start_state)))

    def register_winning_state(self, winning_state):
        self.winning_state = winning_state


    def register_actions(self, action_list):
        self.actions = action_list

    def register_operators(self, op_list):
        self.ops = op_list

    def register_transition_function(self, transition_function):
        self.T = transition_function

    def register_reward_function(self, reward_function):
        self.R = reward_function



    def state_neighbors(self, state):
        '''Return a list of the successors of state.  First check
           in the hash self.succ for these.  If there is no list for
           this state, then construct and save it.
           And then return the neighbors.'''
        stateString = str(self.nptoArray(state))
        neighbors = self.succ.get(stateString, False)
        if neighbors==False:
            neighbors = [op.apply(state) for op in self.ops if op.is_applicable(state)]
            neighbors_array = []
            neighbors_string = []
            for successor in neighbors:
                neighbors_array.append(self.nptoArray(successor))
                neighbors_string.append(str(self.nptoArray(successor)))
            self.succ[stateString] = neighbors
            self.succArray[stateString] = neighbors_array
            self.known_states.update(neighbors_string)
        return neighbors


    def take_action(self, a):
        s = self.current_state
        neighbors = self.state_neighbors(s)
        threshold = 0.0
        rnd = random.uniform(0.0, 1.0)
        r = self.R(s,a,s)
        for sp in neighbors:
            threshold += self.T(s, a, sp)
            if threshold>rnd:
                r = self.R(s, a, sp)
                s = sp
                break
        self.current_state = s
        self.known_states.add(self.current_state)


    def generateAllStates(self):
        OPEN = []
        CLOSED = []
        OPEN.append(self.nptoArray(self.start_state))
        # self.known_states = set()
        count = 0
        while not (self.winning_state in OPEN):
            S = np.asarray(OPEN[0])
            del OPEN[0]
            CLOSED.append(self.nptoArray(S))

            if (self.winning_state in OPEN) or (self.winning_state in CLOSED):
                print("found")
                return None
            self.known_states.add(str(self.nptoArray(S)))
            L = []
            neighbors = self.state_neighbors(S)
            arrayVersion = []
            for successors in neighbors:
                successorsString = self.nptoArray(successors)
                arraySuccessor = str(self.nptoArray(successors))
                if (not successorsString in CLOSED) and (not successorsString in OPEN):
                    arrayVersion.append(arraySuccessor)
                    L.append(self.nptoArray(successors))
            OPEN = L + OPEN
            self.known_states.update(arrayVersion)
            count += 1


    def nptoArray(self, board):
        '''
        Convert np array into list
        '''
        # cubeStateArray = []
        # for i in range(len(board)):
        #     add = []
        #     add.append(board[i].tolist())
        #     cubeStateArray.append(add)
        return np.array(board).tolist()
