import numpy as np
import math

class Cube:

    facedict = {"U":0, "D":1, "F":2, "B":3, "R":4, "L":5}
    dictface = dict([(v, k) for k, v in facedict.items()])
    # normals = [np.array([0., 1., 0.]), np.array([0., -1., 0.]),
    #            np.array([0., 0., 1.]), np.array([0., 0., -1.]),
    #            np.array([1., 0., 0.]), np.array([-1., 0., 0.])]
    # xdirs = [np.array([1., 0., 0.]), np.array([1., 0., 0.]),
    #            np.array([1., 0., 0.]), np.array([-1., 0., 0.]),
    #            np.array([0., 0., -1.]), np.array([0, 0., 1.])]
    colordict = {"w":0, "y":1, "b":2, "g":3, "o":4, "r":5}


    def __init__(self):
        """
        Default creates a flatboard that represents the initial solved state of the rubiks cube.
        """
        self.N = 2
        self.flatBoard = np.array([np.tile(i, (self.N, self.N)) for i in range(6)])
        self.npWinningState = self.flatBoard
        # self.randomize(10)



    def randomize(self, n):
        """
        Make `number` randomly chosen moves to scramble the cube.
        """
        for t in range(n):
            f = self.dictface[np.random.randint(6)]
            l = np.random.randint(self.N)
            d = 1 + np.random.randint(3)
            self.moveCube(f, l, d)
        return None

    def turn(self, f, d):
        """
        Turn whole cube (without making a layer move) around face `f`
        `d` 90-degree turns in the clockwise direction.  Use `d=3` or
        `d=-1` for counter-clockwise.
        """
        for l in range(self.N):
            self.moveCube(f, l, d)
        return None


    def moveCube(self, f, l, d):
        """
        Make a layer move of layer `l` parallel to face `f` through
        `d` 90-degree turns in the clockwise direction.  Layer `0` is
        the face itself, and higher `l` values are for layers deeper
        into the cube.  Use `d=3` or `d=-1` for counter-clockwise
        moves, and `d=2` for a 180-degree move..
        """
        i = self.facedict[f]
        l2 = self.N - 1 - l
        assert l < self.N
        ds = range((d + 4) % 4)
        if f == "U":
            f2 = "D"
            i2 = self.facedict[f2]
            for d in ds:
                self._rotate([(self.facedict["F"], range(self.N), l2),
                              (self.facedict["R"], range(self.N), l2),
                              (self.facedict["B"], range(self.N), l2),
                              (self.facedict["L"], range(self.N), l2)])
        if f == "D":
            return self.moveCube("U", l2, -d)
        if f == "F":
            f2 = "B"
            i2 = self.facedict[f2]
            for d in ds:
                self._rotate([(self.facedict["U"], range(self.N), l),
                              (self.facedict["L"], l2, range(self.N)),
                              (self.facedict["D"], range(self.N)[::-1], l2),
                              (self.facedict["R"], l, range(self.N)[::-1])])
        if f == "B":
            return self.moveCube("F", l2, -d)
        if f == "R":
            f2 = "L"
            i2 = self.facedict[f2]
            for d in ds:
                self._rotate([(self.facedict["U"], l2, range(self.N)),
                              (self.facedict["F"], l2, range(self.N)),
                              (self.facedict["D"], l2, range(self.N)),
                              (self.facedict["B"], l, range(self.N)[::-1])])
        if f == "L":
            return self.moveCube("R", l2, -d)
        for d in ds:
            if l == 0:
                self.flatBoard[i] = np.rot90(self.flatBoard[i], 3)
            if l == self.N - 1:
                self.flatBoard[i2] = np.rot90(self.flatBoard[i2], 1)
        # print("moved", f, l, len(ds))
        return None

    def _rotate(self, args):
        """
        Internal function for the `move()` function.
        """
        a0 = args[0]
        foo = self.flatBoard[a0]
        a = a0
        for b in args[1:]:
            self.flatBoard[a] = self.flatBoard[b]
            a = b
        self.flatBoard[a] = foo
        return None


    def getCubeState(self):
        self.cubeStateArray = []
        for i in range(len(self.flatBoard)):
            add = []
            add.append(self.flatBoard[i].tolist())
            self.cubeStateArray.append(add)
        return self.cubeStateArray


    def __str__(self):
        result = []
        for i in range(len(self.flatBoard)):
            result.append(self.flatBoard[i].tolist())
        return str(result)


class Operator:

    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_trasf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_trasf(s)


def can_move(s):
    'Always true because no restriction on when to move'
    return True

def move(s, f, l, d):
    s.moveCube(f, l, d)
    return s


# Twelve operators for each face. clock wise (cw) and counter clock wise (ccw) turns
UpCWOP = Operator("Up Face Clock Wise Turn",
                    lambda s: can_move(s),
                    lambda s: move(s, "U", 0, 1))

UpCCWOP = Operator("Up Face Counter Close Wise Turn",
                    lambda s: can_move(s),
                    lambda s: move(s, "U", 0, -1))

DownCWOP = Operator("Down Face Clock Wise Turn",
                    lambda s: can_move(s),
                    lambda s: move(s, "D", 0, 1))

DownCCWOP = Operator("Down Face Counter Clock Turn",
                    lambda s: can_move(s),
                    lambda s: move(s, "D", 0, -1))

FrontCWOP = Operator("Front Face Clockwise Turn",
                    lambda s: can_move(s),
                    lambda s: move(s, "F", 0, 1))

FrontCCWOP = Operator("Front Face Counter Clockwise Turn",
                    lambda s: can_move(s),
                    lambda s: move(s, "F", 0, -1))

BackCWOP = Operator("Back Face Clockwise Turn",
                    lambda s: can_move(s),
                    lambda s: move(s, "B", 0, 1))

BackCCWOP = Operator("Back Face Counter Clockwise Turn",
                    lambda s: can_move(s),
                    lambda s: move(s, "B", 0, -1))

LeftCWOP = Operator("Left Face Clock Wise Turn",
                    lambda s: can_move(s),
                    lambda s: move(s, "L", 0, 1))

LeftCCWOP = Operator("Left Face Counter Clockwise Turn",
                    lambda s: can_move(s),
                    lambda s: move(s, "L", 0, -1))

RightCWOP = Operator("Right Face Clockwise Turn",
                     lambda s: can_move(s),
                     lambda s: move(s, "R", 0, 1))


RightCCWOP = Operator("Right Face Counter Clockwise Turn",
                     lambda s: can_move(s),
                     lambda s: move(s, "R", 0, -1))


OPERATORS = [UpCWOP, UpCCWOP, DownCWOP, DownCCWOP,
             FrontCWOP, FrontCCWOP, BackCWOP, BackCCWOP,
             LeftCWOP, LeftCCWOP, RightCWOP, RightCCWOP]

# ex U: U face clockwise turn
#    U': U face counter clockwise turn
ACTIONS = ["U", "U'", "D", "D'", "F", "F'", "B", "B'", "L", "L'", "R", "R'"]

# Winning state in a normal array format
WINNING_STATE = [[[[0, 0], [0, 0]]], [[[1, 1], [1, 1]]], [[[2, 2], [2, 2]]], [[[3, 3], [3, 3]]], [[[4, 4], [4, 4]]],
                 [[[5, 5], [5, 5]]]]

# Gives each move equal probability
P_normal = .083


def T(s, a, sp):
    '''
    Calculate the transition probability for going from state s to state sp after taking
    action a.
    '''
    if s == WINNING_STATE: return 0
    if sp == WINNING_STATE: return 1
    return P_normal




def R(s, a, sp):
    'Returns the reward associated with transitioning from s to sp via action a.'
    if sp == WINNING_STATE: return 1000
    facedict = {"U":0, "D":1, "F":2, "B":3, "R":4, "L":5}
    facepointdict = {"U":0, "D":0, "F":2, "B":0, "R":0, "L":0}
    for key, value in facedict.items():
        count = 0
        point = 0
        for layer in range(len(sp[value])):
            for cube in range(sp[value][layer]):
                if sp[value][layer][cube] == value:
                    count += 1
        point = math.pow(2, count)
        facepointdict.get(key, point)

    totalRewards = 0
    for key in facepointdict.items():
        totalRewards += facepointdict.get(key)
    return totalRewards



if __name__ == "__main__":
    c = Cube()

    print(c.flatBoard)
    # print(c.result)

    c.moveCube("U", 0, -1)
    print(c.flatBoard)



    def generateAllStates(self):
        '''
        Generates all possible states from initial to winning/completed state.
        '''
        OPEN = []
        CLOSED = []
        OPEN.append(self.nptoArray(self.start_state))
        # self.known_states = set()
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



def AStar(initial_state):
    ''' A* search algorithm implemented using a priority queue to store states and total cost.
    Used a counter produced by the itertools.count() function to break ties among states with
    same priority.
    '''
    global COUNT, BACKLINKS
    # TODO: initialze and put first state into
    # priority queue with respective priority
    # add any auxiliary data structures as needed
    OPEN = PriorityQueue()
    counter = count()
    OPEN.put((0 + heuristics(initial_state), counter,  initial_state))
    CLOSED = []
    BACKLINKS[initial_state] = - 1
    gCost = {initial_state.__hash__(): 0}
    while not OPEN.empty():
        S = OPEN.get()
        S = S[2]
        while S in CLOSED:
            S = OPEN.get()
            S = S[2]
        CLOSED.append(S)
        # DO NOT CHANGE THIS SECTION: begining
        if Problem.GOAL_TEST(S):
            print(Problem.GOAL_MESSAGE_FUNCTION(S))
            path = backtrace(S)
            return path, Problem.PROBLEM_NAME
            # DO NOT CHANGE THIS SECTION: end
            # TODO: finish A* implementation
        COUNT += 1
        # if (COUNT % 32) == 0:
        #     print(".", end="")
        #     if (COUNT % 128) == 0:
        #         print("COUNT = " + str(COUNT))
        #         print("len(OPEN)=" + str(len(OPEN)))
        #         print("len(CLOSED)=" + str(len(CLOSED)))
        newGCost = gCost[S.__hash__()] + 1
        for op in Problem.OPERATORS:
            if op.precond(S):
                new_state = op.state_transf(S)
                if not new_state in CLOSED: # Do we need to check open?
                    BACKLINKS[new_state] = S
                    OPEN.put((newGCost + heuristics(S), next(counter), new_state) )
                    gCost[new_state.__hash__()] = newGCost