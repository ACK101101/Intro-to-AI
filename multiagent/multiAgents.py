# multiAgents.py
# --------------
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


from os import stat
from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        oldFood = currentGameState.getFood()
        numOldFood = currentGameState.getNumFood()
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        numNewFood = successorGameState.getNumFood()
        newGhostStates = successorGameState.getGhostStates()
        newGhostPos = successorGameState.getGhostPositions()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        man_dist_food = []                  # distance to all pellets
        for x in range(newFood.width):
            for y in range(newFood.height):
                if newFood[x][y]:
                    man_dist_food.append(util.manhattanDistance(newPos, (x,y)))
        if len(man_dist_food) == 0 or min(man_dist_food) == 0:
            man_dist_food = [0.01]
        if numNewFood == 0:     numNewFood = 1
        food_heur = (numOldFood-numNewFood) + 1/min(man_dist_food)  # bigger with less food and when closer to all pellets

        man_dist_ghost = []
        for x in range(len(newGhostPos)):
            man_dist_ghost.append(util.manhattanDistance(newPos, newGhostPos[x]))
        ghost_heur = 0
        for y in man_dist_ghost:        # avoid close ghosts
            if y == 0:      ghost_heur -= 50
            if y == 1:      ghost_heur -= 10

        win = 0
        if successorGameState.isWin():  win = 5
        
        still_pen = 0
        if action == Directions.STOP:   still_pen -= 10

        return food_heur + ghost_heur + win + still_pen

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        value, action = MinimaxAgent.minimax(self, gameState, 0, self.depth)
        return action           # need to return an action

    def minimax(self, state, agentIndex, depth):   
        if depth == 0 or state.isWin() or state.isLose():
            return self.evaluationFunction(state), 0
        
        if agentIndex == 0:
            actions = state.getLegalActions(agentIndex)          # pacman legal actions
            maxVal, maxAct = -100000000000, 0
            for a in actions:               
                succ = state.generateSuccessor(0, a)    # gen successor for each action
                val, act = MinimaxAgent.minimax(self, succ, agentIndex+1, depth)
                if val > maxVal:    maxVal, maxAct = val, a
            return maxVal, maxAct
        
        if agentIndex > 0:  
            actions = state.getLegalActions(agentIndex)
            minVal, minAct = 100000000000, 0
            for a in actions:
                succ = state.generateSuccessor(agentIndex, a)
                if agentIndex == state.getNumAgents()-1:         # if final ghost 
                    val, act = MinimaxAgent.minimax(self, succ, 0, depth-1)
                else:                                           # if not last ghost 
                    val, act = MinimaxAgent.minimax(self, succ, agentIndex+1, depth)
                if val < minVal:    minVal, minAct = val, a
            return minVal, minAct     

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha, beta = -100000000000, 100000000000
        value, action, al, be, prev = AlphaBetaAgent.alpha_beta(self, gameState, alpha, beta, 0, self.depth)
        return action

    def alpha_beta(self, state, alpha, beta, agentIndex, depth):
        if depth == 0 or state.isWin() or state.isLose():
            return self.evaluationFunction(state), 0, alpha, beta, -1
        
        if agentIndex == 0:
            actions = state.getLegalActions(agentIndex)          # pacman legal actions
            maxVal, maxAct = -100000000000, 0
            for a in actions:               
                succ = state.generateSuccessor(0, a)            # gen successor for each action
                val, act, al, be, prev = AlphaBetaAgent.alpha_beta(self, succ, alpha, beta, agentIndex+1, depth)
                alpha = max(val, alpha)
                if prev > 0:        alpha = max(be, alpha)            # if from ghost -> update alpha
                if val > maxVal:    maxVal, maxAct = val, a
                if alpha > beta:    break
            return maxVal, maxAct, alpha, beta, agentIndex
        
        if agentIndex > 0:  
            actions = state.getLegalActions(agentIndex)
            minVal, minAct = 100000000000, 0
            for a in actions:
                succ = state.generateSuccessor(agentIndex, a)
                if agentIndex == state.getNumAgents()-1:         # if final ghost 
                    val, act, al, be, prev = AlphaBetaAgent.alpha_beta(self, succ, alpha, beta, 0, depth-1)
                else:                                           # if not last ghost 
                    val, act, al, be, prev = AlphaBetaAgent.alpha_beta(self, succ, alpha, beta, agentIndex+1, depth)
                beta = min(val, beta)
                if prev == 0:       beta = min(al, beta)            # if from pac -> update beta
                if val < minVal:    minVal, minAct = val, a
                if alpha > beta:    break
            return minVal, minAct, alpha, beta, agentIndex

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        value, action = ExpectimaxAgent.expectimax(self, gameState, 0, self.depth)
        return action           # need to return an action

    def expectimax(self, state, agentIndex, depth):   
        if depth == 0 or state.isWin() or state.isLose():
            return self.evaluationFunction(state), 0
        
        if agentIndex == 0:
            actions = state.getLegalActions(agentIndex)          # pacman legal actions
            maxVal, maxAct = -100000000000, 0
            for a in actions:               
                succ = state.generateSuccessor(0, a)    # gen successor for each action
                val, act = ExpectimaxAgent.expectimax(self, succ, agentIndex+1, depth)
                if val > maxVal:    maxVal, maxAct = val, a
            return maxVal, maxAct
        
        if agentIndex > 0:  
            actions = state.getLegalActions(agentIndex)
            aveVal, minAct = 0, 0
            for a in actions:
                succ = state.generateSuccessor(agentIndex, a)
                if agentIndex == state.getNumAgents()-1:         # if final ghost 
                    val, act = ExpectimaxAgent.expectimax(self, succ, 0, depth-1)
                else:                                           # if not last ghost 
                    val, act = ExpectimaxAgent.expectimax(self, succ, agentIndex+1, depth)
                aveVal += val
            return aveVal/len(actions), minAct     

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: 
    1) food heuristic :=    gets higher with less food on the grid, 
                            gets higher when closer to all of the pellets
                            gets higher with less power pellets on the grid
    2) ghost heuristic :=   gets a lot lower when very close to a ghost
    3) loss heuristic :=    big loss for being in a loss state
    4) win heuristic :=     reward for being in a win state
    final heuristic = 1 + 2 + 3 + 4
    """
    "*** YOUR CODE HERE ***"
    food = currentGameState.getFood()
    numFood = currentGameState.getNumFood()
    pacPos = currentGameState.getPacmanPosition()
    pacDir = currentGameState.getPacmanState().getDirection()
    ghostStates = currentGameState.getGhostStates()
    ghostPos = currentGameState.getGhostPositions()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    pellet = currentGameState.getCapsules()
    numPellet = len(pellet)

    man_dist_food = []                  # distance to all pellets
    for x in range(food.width):
        for y in range(food.height):
            if food[x][y]:
                man_dist_food.append(util.manhattanDistance(pacPos, (x,y)))
    
    if numFood == 0:               numFood = 0.1
    if len(man_dist_food) == 0:         man_dist_food = [0.1]
    if numPellet == 0:             numPellet = 0.1

    food_heur = 100/numFood + 1000/sum(man_dist_food) + 1/numPellet

    man_dist_ghost = []
    for x in range(len(ghostPos)):
        man_dist_ghost.append(util.manhattanDistance(pacPos, ghostPos[x]))
    ghost_heur = 0
    for y in man_dist_ghost:        # avoid close ghosts
        if y == 0:      ghost_heur -= 500
        if y == 1:      ghost_heur -= 100
    
    loss = 0
    if currentGameState.isLose(): loss = -100
    win = 0
    if currentGameState.isWin():  win = 10

    return food_heur + ghost_heur + win + loss + random.randrange(0, 2)
     
# Abbreviation
better = betterEvaluationFunction
