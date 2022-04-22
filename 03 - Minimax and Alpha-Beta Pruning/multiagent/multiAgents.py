
from pacman import GameState
from game import Agent


def evaluation_function(gamestate: GameState):
    """
    This evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.
    """
    return gamestate.getScore()


class MultiAgentSearchAgent(Agent):

    def __init__(self, depth='2'):
        self.index = 0  # Pacman is always agent with index 0
        self.evaluationFunction = evaluation_function
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """ Agent for Question 2 """

    def getAction(self, state: GameState):
        _, action = self.minimax(state, agent_index=0, depth=self.depth)
        return action

    def stop_recursion(self, gamestate: GameState, depth: int) -> bool:
        """ 
        Checks if the recursion has reached the bottom depth or if the state is in a finsished state
        """
        return depth == 0 or gamestate.isWin() or gamestate.isLose()

    def is_maximizing_player(self, agent_index: int) -> bool:
        """ 
        Check if the current `agent_index` should maximize or minimize the value 
        """
        return agent_index == self.index  # self.index == pacmans index

    # This minimax implementation is inspired by Sebastian Lague's video: https://www.youtube.com/watch?v=l-hh51ncgDI&ab_channel=SebastianLague
    def minimax(self, gamestate: GameState, agent_index: int, depth: int) -> 'tuple[int, str]':
        """ 
        Return the optimal score and action to perform in the given state for the given agent

        Returns:
            `int, str`: [score, action]
        """
        # Increase depth when it is pacman's (agent_index=0) turn (when we have gone through all agents)
        if agent_index == gamestate.getNumAgents():
            agent_index = self.index  # start from pacman again
            depth -= 1  # dig deeper

        # If we have reached our end leaves, return the value for that leaf
        if self.stop_recursion(gamestate, depth):
            return self.evaluationFunction(gamestate), None

        # Get all legal actions for our current agent
        actions = gamestate.getLegalActions(agent_index)

        if self.is_maximizing_player(agent_index):
            # The maximizing agent wants to perform the action that results in the highest possible score
            # In our environment this agent is always PacMan.

            # Initilize with pacmans worst possible values
            best_action = None
            highest_score = -float('inf')  # - infinity

            # go though each of pacmans actions and determine the action with the highest score
            for action in actions:
                next_state = gamestate.generateSuccessor(agent_index, action)
                score, _ = self.minimax(next_state, agent_index + 1, depth)
                if (score > highest_score):
                    highest_score, best_action = score, action
            # Return the highest score, and the action that yields that score
            return highest_score, best_action

        else:
            # The minimizing agents (ghosts) perform actions we can't control, we therfore only worry about
            # score here. We assume the ghosts perform the action that is the worst for us (leads to the
            # lowest score).

            # Initialize with the ghosts worst possible resulting score (high score for pacman)
            lowest_score = float('inf')  # + infinity

            # Go though all of this ghost's actions and keep track of the lowest score
            for action in actions:
                next_state = gamestate.generateSuccessor(agent_index, action)
                score, _ = self.minimax(next_state, agent_index + 1, depth)
                if (score < lowest_score):
                    lowest_score = score
            # We only care about the score here because we have no control over
            # what action the ghost will perform, we only assume the worst.
            return lowest_score, None


class AlphaBetaAgent(MinimaxAgent):
    """ Agent for Question 3 """

    def getAction(self, state: GameState):
        # Initialize worst case for max and min agents
        alpha = -float('inf')
        beta = float('inf')

        _, action = self.alpha_beta(state, 0, self.depth, alpha, beta)
        return action

    def prune(self, alpha, beta) -> bool:
        """ 
        We know we can prune when `alpha` > `beta` because alpha and beta keep track of best values we have
        found so far. We can think of it as if the alpha and beta keeps track of what node we have checked
        the other agent is going to choose. 

        This means that for our maximizing agent (Pacman), if he first checks an action that is very bad for him,
        when we go through the children of the next action, the moment we see that this action is better than the 
        one we have before, we stop looking at this action. This is a little counterintuitive because pacman wants
        to maximize his score right? We are essentially using the knowledge that the ghosts will select the action
        that is worst for pacman, and hence, will choose the bad action we already found no matter what scores
        we continue to find for the other action.

        And for our minimizing agents (ghosts), it means that pacman has already found an action 
        better than the one we are currently checking, so we dont need to calculate further because
        pacman never will select this action anyway.
        """
        return alpha > beta

    # This minimax implementation is inspired by Sebastian Lague's video: https://www.youtube.com/watch?v=l-hh51ncgDI&ab_channel=SebastianLague
    def alpha_beta(self, gamestate: GameState, agent_index: int, depth: int, alpha, beta) -> 'tuple[int, str]':
        """ 
        Return the optimal score and action to perform in the given state for the given agent

        The method i almost exactly the same as `minimax()`, so look at that function for more in depth comments 

            `alpha`: the minimum score that the maximizing player is guaranteed    
            `beta`: the maximum score that the minimizing player is guaranteed     

        Returns:
            `int, str`: [score, action]
        """
        if agent_index == gamestate.getNumAgents():
            agent_index = self.index
            depth -= 1

        if self.stop_recursion(gamestate, depth):
            return self.evaluationFunction(gamestate), None

        actions = gamestate.getLegalActions(agent_index)

        if self.is_maximizing_player(agent_index):
            best_action = None
            highest_score = -float('inf')  # - infinity

            for action in actions:
                next_state = gamestate.generateSuccessor(agent_index, action)
                score, _ = self.alpha_beta(
                    next_state, agent_index + 1, depth, alpha, beta)

                if (score > highest_score):
                    highest_score, best_action = score, action
                    # Check if this score is better than any we have found before
                    alpha = max(alpha, score)

                if self.prune(alpha, beta):
                    # Stop checking future actions for this node
                    break

            return highest_score, best_action

        else:
            lowest_score = float('inf')  # + infinity

            for action in actions:
                next_state = gamestate.generateSuccessor(agent_index, action)
                score, _ = self.alpha_beta(
                    next_state, agent_index + 1, depth, alpha, beta)

                if (score < lowest_score):
                    lowest_score = score
                    # check if this score is worse than any we have found before
                    beta = min(beta, score)

                if self.prune(alpha, beta):
                    # Stop checking future actions for this node
                    break

            return lowest_score, None
