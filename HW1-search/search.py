# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

#from importlib.resources import path
#from turtle import pos
import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    # init action stack in parallel with frontier
    actions = util.Stack()
    actions.push([])
    visited = {}

    # init queue (stack) with start state
    start = problem.getStartState()
    frontier = util.Stack()
    frontier.push(start)

    # while loop to go through frontier until goal or empty
    while frontier.isEmpty() == False:
        n = frontier.pop()
        path_so_far = actions.pop()

        # check if popped is goal
        if problem.isGoalState(n) == True:
            #print("Len of sol path: ", len(path_so_far))
            return path_so_far

        # add to visited when expanded
        visited[n] = 0

        # expand node
        for s in problem.getSuccessors(n):
            # discard visited and add non-visited to queue
            if s[0] not in visited:
                poss_path = path_so_far.copy()
                poss_path.append(s[1])
                # maintain action and frontier queue in parallel
                actions.push(poss_path)
                frontier.push(s[0])
        


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    # init action stack in parallel with frontier
    actions = util.Queue()
    actions.push([])
    visited = {}

    # init queue (stack) with start state
    start = problem.getStartState()
    #print("Start: ", start)
    frontier = util.Queue()
    frontier.push(start)

    # while loop to go through frontier until goal or empty
    while frontier.isEmpty() == False:
        n = frontier.pop()
        #print("N: ", n)
        path_so_far = actions.pop()
        #print("Path so far: ", path_so_far)
        
        # check if popped is goal
        if problem.isGoalState(n) == True:
            #print("Len of sol path: ", len(path_so_far))
            return path_so_far

        # expand node if not visited
        if n not in visited:
            visited[n] = 0
            for s in problem.getSuccessors(n):
                # children to queue
                poss_path = path_so_far.copy()
                poss_path.append(s[1])
                # maintain action and frontier queue in parallel
                actions.push(poss_path)
                frontier.push(s[0])
                

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    # 0: frontier, 1: path, 2: cost
    queue = util.PriorityQueue()
    queue.push([problem.getStartState(), [], 0], 0)
    visited = {}

    # while loop to go through frontier until goal or empty
    while queue.isEmpty() == False:
        pop = queue.pop()
        n, path_so_far, cost_so_far = pop[0], pop[1], pop[2]
        
        # check if popped is goal
        if problem.isGoalState(n) == True:
            #print("Len of sol path: ", len(path_so_far))
            return path_so_far

        # expand node if not visited
        if n not in visited:
            visited[n] = 0
            for s in problem.getSuccessors(n):
                # add children to queue
                poss_path = path_so_far.copy()
                poss_path.append(s[1])
                #
                poss_cost = 0
                poss_cost += cost_so_far + s[2]
                # maintain action and frontier queue in parallel
                queue.push([s[0], poss_path, poss_cost], poss_cost)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    """Search the node of least total cost first."""
    # 0: frontier, 1: path, 2: cost
    queue = util.PriorityQueue()
    queue.push([problem.getStartState(), [], 0], 0)
    visited = {}

    # while loop to go through frontier until goal or empty
    while queue.isEmpty() == False:
        pop = queue.pop()
        n, path_so_far, cost_so_far = pop[0], pop[1], pop[2]
        
        # check if popped is goal
        if problem.isGoalState(n) == True:
            # print("Len of sol path: ", len(path_so_far))
            return path_so_far

        # expand node if not visited
        if n not in visited:
            visited[n] = 0
            for s in problem.getSuccessors(n):
                if s[0] not in visited:
                    # add children to queue
                    poss_path = path_so_far.copy()
                    poss_path.append(s[1])
                    #
                    poss_cost = 0
                    poss_cost += cost_so_far + s[2]
                    man_dist = heuristic(s[0], problem)
                    # maintain action and frontier queue in parallel
                    queue.push([s[0], poss_path, poss_cost], man_dist + poss_cost)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
