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
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    # super an ordinary stack for DFS
    dfs_stack = util.Stack()

    # set the initial status
    explored = set()
    frontier = []
    initial_state = problem.getStartState()

    actions = []
    dfs_stack.push((initial_state, actions, 0))
    frontier.append(initial_state)

    while not dfs_stack.isEmpty():
        current_state, actions, cost = dfs_stack.pop()
        frontier.pop()

        if problem.isGoalState(current_state):
            return actions

        if current_state not in explored:
            explored.add(current_state)
            successors = problem.getSuccessors(current_state)

            for successor in successors:
                successor_state, successor_action, successor_cost = successor
                # graph search
                if successor_state in explored:
                    continue
                if successor_state in frontier:
                    continue
                successor_actions = actions + [successor_action]
                successor_cost += cost

                dfs_stack.push((successor_state, successor_actions, successor_cost))
                frontier.append(successor_state)

    return []  # path note found
    # util.raiseNotDefined()


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # super an ordinary queue for BFS
    bfs_queue = util.Queue()

    # set the initial status
    explored = set()
    frontier = []
    initial_state = problem.getStartState()

    actions = []
    bfs_queue.push((initial_state, actions, 0))
    frontier.append(initial_state)

    while not bfs_queue.isEmpty():
        # get the info of current path
        current_state, actions, cost = bfs_queue.pop()
        frontier.pop(0)

        # goal state detection
        if problem.isGoalState(current_state):
            return actions

        if current_state not in explored:
            explored.add(current_state)

            successors = problem.getSuccessors(current_state)

            for successor in successors:
                successor_state, successor_action, successor_cost = successor
                # graph search
                if successor_state in explored:
                    continue
                if successor_state in frontier:
                    continue
                successor_actions = actions + [successor_action]
                successor_cost += cost

                bfs_queue.push((successor_state, successor_actions, successor_cost))
                frontier.append(successor_state)

    return []  # path note found
    # util.raiseNotDefined()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # super an ordinary queue for UCS
    ucs_queue = util.PriorityQueue()

    # set the initial status
    explored = set()
    initial_state = problem.getStartState()
    # class node for frontier check
    initial_node = Node(initial_state, None, 0, '')

    ucs_queue.update(initial_node, priority=0)

    while not ucs_queue.isEmpty():
        # get the info of current path
        current_node = ucs_queue.pop()
        current_state = current_node.state
        current_cost = current_node.path_cost

        # goal state detection
        if problem.isGoalState(current_state):
            return current_node.solution()

        if current_state not in explored:
            explored.add(current_state)

            successors = problem.getSuccessors(current_state)

            for successor in successors:
                successor_state, successor_action, successor_cost = successor
                # graph search
                if successor_state in explored:
                    continue

                successor_node = Node(successor_state,
                                      current_node,
                                      current_cost+successor_cost,
                                      successor_action)

                ucs_queue.update(successor_node, priority=successor_node.path_cost)

    return []  # path note found
    # util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # super an ordinary queue for UCS
    ucs_queue = util.PriorityQueue()

    # set the initial status
    explored = set()
    initial_state = problem.getStartState()
    initial_node = Node(initial_state, None, 0, '')

    ucs_queue.update(initial_node, priority=0)

    while not ucs_queue.isEmpty():
        # get the info of current path
        current_node = ucs_queue.pop()
        current_state = current_node.state
        current_cost = current_node.path_cost

        # goal state detection
        if problem.isGoalState(current_node.state):
            return current_node.solution()

        if current_state not in explored:
            explored.add(current_state)

            successors = problem.getSuccessors(current_state)

            for successor in successors:
                successor_state, successor_action, successor_cost = successor
                # graph search
                if successor_state in explored:
                    continue

                successor_node = Node(successor_state,
                                      current_node,
                                      current_cost+successor_cost,
                                      successor_action)
                heuristic_value = heuristic(successor_state, problem=problem)

                ucs_queue.update(successor_node,
                                 priority=successor_node.path_cost + heuristic_value)

    return []  # path note found
    # util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch


######################################
# Add by Shun Zhang bellow this line #
######################################


class Node:

    def __init__(self, state, parent, path_cost, action):
        self.state = state
        self.parent = parent  # parent is also a node
        self.path_cost = path_cost
        self.action = action  # the action from parent

    def __eq__(self, other):
        return self.state == other.state

    def solution(self):
        position = self
        path = []
        while position.parent is not None:
            path.insert(0, position.action)
            position = position.parent
        return path
