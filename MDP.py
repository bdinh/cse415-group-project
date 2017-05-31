'''
Bao Dinh, Andrew Kan, Chris Oh
CSE 415
Project
'''

import random
import copy
import numpy as np
import ast
import math
from queue import PriorityQueue
from itertools import count


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
        # neighbors = self.get_neighbors(str(s))
        neighbors = self.state_neighbors(s)
        threshold = 0.0
        rnd = random.uniform(0.0, 1.0)
        r = self.R(s, a, s)
        for sp in neighbors:
            arraySp = self.nptoArray(sp)
            threshold += self.T(s, a, arraySp)
            if threshold > rnd:
                r = self.R(s, a, arraySp)
                s = arraySp
                break
                # succ = self.state_neighbors(np.asarray(s))
        self.current_state = s
        self.known_states.add(str(self.current_state))




    def generateAllStates(self):
        '''
        Generates all possible states from initial to winning/completed state.
        '''
        OPEN = []
        CLOSED = []
        OPEN.append(self.nptoArray(self.start_state))
        count = 0
        while not (self.winning_state in OPEN):
            S = np.asarray(OPEN[0])
            del OPEN[0]
            CLOSED.append(self.nptoArray(S))
            self.known_states.add(str(self.nptoArray(S)))
            L = []
            neighbors = self.state_neighbors(S)
            arrayVersion = []
            for successors in neighbors:
                successorsString = self.nptoArray(successors)
                arraySuccessor = str(self.nptoArray(successors))
                if not successorsString in OPEN:
                    arrayVersion.append(arraySuccessor)
                    L.append(self.nptoArray(successors))
            OPEN = OPEN + L
            self.known_states.update(arrayVersion)
            count += 1

    def nptoArray(self, board):
        '''
        Convert np array into list
        '''
        return np.array(board).tolist()

    def valueIteration(self, discount, iterations):
        self.V = {}
        for state in self.known_states:
            self.V[state] = 0
        for i in range(iterations):
            dictionary = self.V.copy()
            for state, succ in self.succArray.items():
                neighbors = succ.copy()
                transition, reward = self.T, self.R
                keyState = ast.literal_eval(state)
                keyState = np.asarray(keyState)
                neighbors.append(keyState)
                maxActionValue = -99999
                for action in self.actions:
                    result = 0
                    for endState in neighbors:
                        keyEndState = str(self.nptoArray(endState))
                        result += transition(keyState, action, endState) * (reward(keyState, action, endState) + discount*dictionary.get(keyEndState))
                    if result > maxActionValue:
                        maxActionValue = result
                self.V[state] = maxActionValue


    def QLearning(self, discount, nEpisode, epsilon):
        self.QValues = {}
        actionCounter = {}
        self.Q = self.QValues
        reward = self.R

        for state in self.known_states:
            for action in self.actions:
                self.QValues[(state, action)] = 0
                actionCounter[(state, action)] = 0


        for i in range(nEpisode):

            self.current_state = self.nptoArray(self.start_state) # array not string

            while self.current_state != self.winning_state:
                possibleAction = {}
                for action in self.actions:

                    possibleAction[action] = self.Q.get((str(self.current_state), action), 0)
                randomAction = random.uniform(0,1)
                if randomAction < epsilon:
                    bestAction = self.actions[random.randint(0, len(self.actions) - 1)]
                else:
                    # Grabs best key from possible actions
                    # Assisted using https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
                    bestAction = max(possibleAction, key=possibleAction.get)
                alphaCount = actionCounter.get((str(self.current_state), bestAction), 0) + 1
                actionCounter[(str(self.current_state), bestAction)] = alphaCount
                learningRate = 1 / alphaCount
                oldState = self.current_state
                self.take_action(bestAction[0])
                newAction = {}
                for action in self.actions:
                    tup = (str(self.current_state), action)
                    newAction[action] = self.QValues.get(tup, 0)
                maxAction = max(newAction, key=newAction.get)
                result = (1 - learningRate) * self.Q.get((str(oldState), bestAction), 0) + learningRate * (reward(oldState, bestAction, self.current_state) + discount*newAction[maxAction])
                self.Q[str(oldState), bestAction] = result
            self.QValues = self.Q

    def get_neighbors(self, key):
        neighbors = []
        for state, succ in self.succArray.items():
            if str(state) == key:
                return succ
        return neighbors

    def colorPoints(self, sp):
        if sp == self.winning_state: return 1000
        facedict = {"U":0, "D":1, "F":2, "B":3, "R":4, "L":5}
        facepointdict = {"U":0, "D":0, "F":2, "B":0, "R":0, "L":0}
        for key, value in facedict.items():
            count = 0
            point = 0
            for layer in range(len(sp[value])):
                for cube in range(len(sp[value][layer])):
                    if sp[value][layer][cube] == value:
                        count += 1
            point = math.pow(2, count)
            facepointdict[key] = point
        totalRewards = 0
        for key,value in facepointdict.items():
            totalRewards += facepointdict[key]
        return totalRewards


    def generateAllStatesWithHeuristics(self):
        COUNT = 0
        OPEN = PriorityQueue()
        CLOSED = []
        counter = count()
        arrayStartingState = self.nptoArray(self.start_state)
        OPEN.put((0 + self.colorPoints(arrayStartingState), 0, str(self.nptoArray(self.start_state))))
        gCost = {str(self.nptoArray(self.start_state)): 0}
        self.backlink = {}
        self.backlink[str(self.nptoArray(self.start_state))] = ("NA", -1)
        while not self.winning_state in CLOSED:
            S = OPEN.get()
            S = ast.literal_eval(S[2]) # currently in an array
            CLOSED.append(S)
            neighbors = self.state_neighbors(np.asarray(S))
            arrayVersion = []
            newGCost = gCost[str(S)] + 1
            COUNT += 1
            actionCount = 0
            for successors in neighbors:
                arraySuccessor = self.nptoArray(successors)
                successorsString = str(arraySuccessor)
                if not (arraySuccessor in CLOSED):
                    # str(S)
                    self.backlink[successorsString] = (self.actions[actionCount], str(S))
                    test = (newGCost + -self.colorPoints(arraySuccessor), next(counter), successorsString)
                    OPEN.put(test)
                    gCost[successorsString] = newGCost
                    arrayVersion.append(successorsString)
                actionCount += 1
            self.known_states.add(str(S))


    def extractBestMove(self):
        bestAction = None
        bestValue = -99999
        for key, value in self.QValues.items():
            if value > bestValue:
                bestValue = value
                bestAction = key[1]
        return bestAction




    def get_state_neighbors(self, state):
        stateString = str(self.nptoArray(state))
        neighbors = self.succ.get(stateString, False)
        if neighbors==False:
            neighbors = [op.apply(state) for op in self.ops if op.is_applicable(state)]
            # neighbors_string = []
        neighbors_actions = []
        for i in range(len(neighbors)):
            string = str(self.nptoArray(neighbors[i]))
            tup = (string, self.actions[i])
            neighbors_actions.append(tup)
        return neighbors_actions