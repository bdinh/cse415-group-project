import numpy as np
import math

facedict = {"U": 0, "D": 1, "F": 2, "B": 3, "R": 4, "L": 5}
dictface = dict([(v, k) for k, v in facedict.items()])
colordict = {"w": 0, "y": 1, "b": 2, "g": 3, "o": 4, "r": 5}
N = 2
initial_board = np.array([np.tile(i, (N, N)) for i in range(6)])

def createInitialCube():
    '''
    Create a random initial cube(2x2) through an array that represents the cube layed out flatly
    '''
    global initial_board
    initial_board = move(initial_board, "U", 0, 1)
    # print(str(nptoArray(initial_board)))



def randomize(board, n):
    """
    Make `number` randomly chosen moves to scramble the cube.
    """
    global N, dictface
    for t in range(n):
        f = dictface[np.random.randint(6)]
        # l = np.random.randint(N)
        # d = 1 + np.random.randint(3)
        d = np.random.randint(2)
        if d == 0:
            d = -1
        moveCube(board, f, 0, d)
    return board

def moveCube(board, f, l, d):
    """
    Make a layer move of layer `l` parallel to face `f` through
    `d` 90-degree turns in the clockwise direction.  Layer `0` is
    the face itself, and higher `l` values are for layers deeper
    into the cube.  Use `d=3` or `d=-1` for counter-clockwise
    moves, and `d=2` for a 180-degree move..
    """
    global facedict, N
    print(l)
    i = facedict[f]
    l2 = N - 1 - l
    assert l < N
    ds = range((d + 4) % 4)
    if f == "U":
        f2 = "D"
        i2 = facedict[f2]
        for d in ds:
            rotate(board, [(facedict["F"], range(N), l2),
                          (facedict["R"], range(N), l2),
                          (facedict["B"], range(N), l2),
                          (facedict["L"], range(N), l2)])
    if f == "D":
        return moveCube(board, "U", l2, -d)
    if f == "F":
        f2 = "B"
        i2 = facedict[f2]
        for d in ds:
            rotate(board, [(facedict["U"], range(N), l),
                          (facedict["L"], l2, range(N)),
                          (facedict["D"], range(N)[::-1], l2),
                          (facedict["R"], l, range(N)[::-1])])
    if f == "B":
        return moveCube(board, "F", l2, -d)
    if f == "R":
        f2 = "L"
        i2 = facedict[f2]
        for d in ds:
            rotate(board, [(facedict["U"], l2, range(N)),
                          (facedict["F"], l2, range(N)),
                          (facedict["D"], l2, range(N)),
                          (facedict["B"], l, range(N)[::-1])])
    if f == "L":
        return moveCube(board, "R", l2, -d)
    for d in ds:
        if l == 0:
            board[i] = np.rot90(board[i], 3)
        if l == N - 1:
            board[i2] = np.rot90(board[i2], 1)
    print("moved", f, l, len(ds))
    return board

def rotate(board, args):
    """
    Internal function for the `move()` function.
    """
    a0 = args[0]
    foo = board[a0]
    a = a0
    for b in args[1:]:
        board[a] = board[b]
        a = b
    board[a] = foo
    return board


def nptoArray(board):
    '''
    Convert np array into list
    '''
    # cubeStateArray = []
    # for i in range(len(board)):
    #     add = []
    #     add.append(board[i].tolist())
    #     cubeStateArray.append(add)
    return np.array(board).tolist()



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
    'Always true because no restriction on if move is legal'
    return True

def move(s, f, l, d):
    new = s.__copy__()
    new = moveCube(new, f, l, d)
    return new

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
WINNING_STATE = [[[0, 0], [0, 0]], [[1, 1], [1, 1]], [[2, 2], [2, 2]], [[3, 3], [3, 3]], [[4, 4], [4, 4]], [[5, 5], [5, 5]]]




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


# if __name__ == "__main__":


