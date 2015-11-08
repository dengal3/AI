# -*- coding: UTF-8 -*-
# author: ailin
# hill climb
# based on 8-queen
import copy
import random

class Node:
    """state node for 8-queen"""
    def __init__(self, problem):
        self.queens = []
        for queen in problem:
            self.queens.append({
                "x": queen[0],
                "y": queen[1]
            })


"""hill climb(random start)"""
def randomStartHillClimbing(problem):
    current, best = [], []
    #print "problem: ", problem
    current = Node(problem)
    #print "current: ", current.queens
    
    while True:
        best = getHighestValuedSuccessorOfCurrent(current)
        if getValue(best) >= getValue(current):
            # if not success try and try again
            if getValue(current) != 0:
                current = randomGenerateNode()
            else:
                return current
        else:
            current = copy.deepcopy(best)
            current.queens = copy.deepcopy(best.queens)

"""random generate a new state"""
def randomGenerateNode():
    newProblem = []
    for col, num in enumerate(random.sample([i for i in xrange(8)], 8)):
        newProblem.append([num, col])
    return Node(newProblem)

"""the hightest one get the lowest value"""
def getHighestValuedSuccessorOfCurrent(current):
    result = []
    for i, neighbor in enumerate(getAllNeighbors(current)):
        if not i or getValue(neighbor) <= getValue(result):
            result = neighbor
    return result


"""get all available node(state) besides the current node"""
def getAllNeighbors(current):
    neighbors = []
    operations = [{"x": 1, "y": 0}, {"x": -1, "y": 0},
                 {"x": 2, "y": 0}, {"x": -2, "y": 0},
                 {"x": 3, "y": 0}, {"x": -3, "y": 0},
                 {"x": 4, "y": 0}, {"x": -4, "y": 0},
                 {"x": 5, "y": 0}, {"x": -5, "y": 0},
                 {"x": 6, "y": 0}, {"x": -6, "y": 0},
                 {"x": 7, "y": 0}, {"x": -7, "y": 0}]
    node = copy.deepcopy(current)
    node.queens = copy.deepcopy(current.queens)
    for queen in node.queens:
        for operation in operations:
            if isValid(queen, operation):
                action(queen, operation)
                newNode = copy.deepcopy(node)
                newNode.queens = copy.deepcopy(node.queens)
                neighbors.append(newNode)
                reaction(queen, operation)
    return neighbors

def isValid(queen, operation):
    return (queen["x"] + operation["x"] >= 0 and queen["x"] + operation["x"] < 8) and (queen["y"] + operation["y"] >= 0 and queen["y"] + operation["y"] < 8)

def action(queen, operation):
    queen["x"] += operation["x"]
    queen["y"] += operation["y"]

def reaction(queen, operation):
    queen["x"] -= operation["x"]
    queen["y"] -= operation["y"]


def getValue(node):
    h = 0
    for queen in node.queens:
        for sub_queen in node.queens:
            if sub_queen is not queen and isConflicted(queen, sub_queen):
                h += 1
    return h/2

def isConflicted(queen, other):
    return queen["x"] == other["x"] or queen["y"] == other["y"] or abs(queen["x"]-other["x"]) == abs(queen["y"]-other["y"])
    
def normalize(problem):
    output = []
    for i, num in enumerate(problem):
        output.append([int(num), i])
    return output

def main():
    f = open("test.txt", "r")
    count = 0
    amount = 0
    for line in f:
        amount += 1
        problem = line.split()  # read in 0 2 1 3 5 6 4 7
        problem = normalize(problem)   # formate the data above to the coordinate form
        
        result = randomStartHillClimbing(problem)
        if getValue(result) == 0:
            count += 1
            print "result:----------"
            for queen in result.queens:
                print queen
    f.close()
    print "All input tests: ", amount
    print "Successful tests: ", count, "("+str(float(count)/amount)+")"

if __name__ == "__main__":
    main()
