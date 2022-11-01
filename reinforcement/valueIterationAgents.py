# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()                               # get all states
        
        for state in states:
            self.values[state] = 0                                  # init all states to 0

        curr_iter = 1
        while curr_iter <= self.iterations:  
            
            values_copy = self.values.copy()                            # keep prev iter values

            # update
            for state in states:
                if not self.mdp.isTerminal(state):
                    actions = self.mdp.getPossibleActions(state)    # get poss actions in state

                    bellman_actions = []
                    for action in actions:
                        states_probs_pairs_list = self.mdp.getTransitionStatesAndProbs(state, action)       # get prob dist of being in s' for taking a in s
                        
                        poss_vals = []
                        for pair in states_probs_pairs_list:
                            next_state = pair[0]
                            prob = pair[1]
                            poss_val = prob * (self.mdp.getReward(state, action, next_state) + (self.discount * values_copy[next_state]))      # value of a in s (given noise)
                            poss_vals.append(poss_val)
                        
                        bellman_poss_act = sum(poss_vals)           # expected value of a in s
                        bellman_actions.append(bellman_poss_act)
                    
                    self.values[state] = max(bellman_actions)       # best a in s -> update values
            
            curr_iter += 1 


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        states_probs_pairs_list = self.mdp.getTransitionStatesAndProbs(state, action)       # get prob dist of being in s' for taking a in s

        poss_vals = []
        for pair in states_probs_pairs_list:
            next_state = pair[0]
            prob = pair[1]
            poss_val = prob * (self.mdp.getReward(state, action, next_state) + (self.discount * self.values[next_state]))      # value of a in s (given noise)
            poss_vals.append(poss_val)
        
        bellman_poss_act = sum(poss_vals)           # expected value of a in s 
        
        return bellman_poss_act

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        actions = self.mdp.getPossibleActions(state)
        
        action_vals = util.Counter()
        for action in actions:
            states_probs_pairs_list = self.mdp.getTransitionStatesAndProbs(state, action)       # get prob dist of being in s' for taking a in s

            poss_vals = []
            for pair in states_probs_pairs_list:
                next_state = pair[0]
                prob = pair[1]
                poss_val = prob * self.values[next_state]      # value of a in s (given noise)
                poss_vals.append(poss_val)
            
            bellman_poss_act = sum(poss_vals)           # expected value of a in s 
            action_vals[action] = bellman_poss_act

        return action_vals.argMax() 

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()                               # get all states
        
        for state in states:
            self.values[state] = 0                                  # init all states to 0
        
        curr_iter = 1
        while curr_iter < self.iterations:  

            # update
            state = states[curr_iter % len(states)]

            if not self.mdp.isTerminal(state):
                actions = self.mdp.getPossibleActions(state)    # get poss actions in state

                bellman_actions = []
                for action in actions:
                    states_probs_pairs_list = self.mdp.getTransitionStatesAndProbs(state, action)       # get prob dist of being in s' for taking a in s
                    
                    poss_vals = []
                    for pair in states_probs_pairs_list:
                        next_state = pair[0]
                        prob = pair[1]
                        poss_val = prob * (self.mdp.getReward(state, action, next_state) + (self.discount * self.values[next_state]))      # value of a in s (given noise)
                        poss_vals.append(poss_val)
                    
                    bellman_poss_act = sum(poss_vals)           # expected value of a in s
                    bellman_actions.append(bellman_poss_act)
                
                self.values[state] = max(bellman_actions)       # best a in s -> update values
        
            curr_iter += 1 


class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

