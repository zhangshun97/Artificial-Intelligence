import util, math, random
from collections import defaultdict
from util import ValueIteration
import argparse

parser = argparse.ArgumentParser(description='for 4b & 4d in blackjack')
parser.add_argument('--p-4b', type=str, default='', metavar='S',
                    help="whether run problem 4b small or large")
parser.add_argument('--p-4d', type=bool, default=False, metavar='B',
                    help='whether run problem 4d')
args = parser.parse_args()


############################################################
# Problem 2a

# If you decide 2a is true, prove it in blackjack.pdf and put "return None" for
# the code blocks below.  If you decide that 2a is false, construct a counterexample.
class CounterexampleMDP(util.MDP):
    def startState(self):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return 0
        # END_YOUR_CODE

    # Return set of actions possible from |state|.
    def actions(self, state):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return [1, -1] if state == 0 else [state]
        # END_YOUR_CODE

    # Return a list of (newState, prob, reward) tuples corresponding to edges
    # coming out of |state|.
    def succAndProbReward(self, state, action):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return [(1, 0.3, 100), (-1, 0.7, -100)] if state == 0 else [(state, 1, 0)]
        # END_YOUR_CODE

    def discount(self):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return 1
        # END_YOUR_CODE


############################################################
# Problem 3a

class BlackjackMDP(util.MDP):
    def __init__(self, cardValues, multiplicity, threshold, peekCost):
        """
        cardValues: array of card values for each card type
        multiplicity: number of each card type
        threshold: maximum total before going bust
        peekCost: how much it costs to peek at the next card
        """
        self.cardValues = cardValues
        self.multiplicity = multiplicity
        self.threshold = threshold
        self.peekCost = peekCost

    # Return the start state.
    # Look at this function to learn about the state representation.
    # The first element of the tuple is the sum of the cards in the player's
    # hand.
    # The second element is the index (not the value) of the next card, if the player peeked in the
    # last action.  If they didn't peek, this will be None.
    # The final element is the current deck.
    def startState(self):
        return (
            0, None,
            (self.multiplicity,) * len(self.cardValues))  # total, next card (if any), multiplicity for each card

    # Return set of actions possible from |state|.
    # You do not need to modify this function.
    # All logic for dealing with end states should be done in succAndProbReward
    def actions(self, state):
        return ['Take', 'Peek', 'Quit']

    # Return a list of (newState, prob, reward) tuples corresponding to edges
    # coming out of |state|.  Indicate a terminal state (after quitting or
    # busting) by setting the deck to None. 
    # When the probability is 0 for a particular transition, don't include that 
    # in the list returned by succAndProbReward.
    def succAndProbReward(self, state, action):
        # BEGIN_YOUR_CODE (our solution is 53 lines of code, but don't worry if you deviate from this)
        current_value, peek_index, current_deck = state
        # check if run out of deck and END the game
        if current_deck is None:
            return []
        prob = 1 / math.fsum(current_deck)
        list2return = []

        if action == 'Quit':
            list2return.append(((current_value, None, None), 1, current_value))
        elif action == 'Take':
            # peeked
            if peek_index is not None:
                reward = 0  # bust and default reward
                card_value = self.cardValues[peek_index]
                new_value = current_value + card_value
                if current_value + card_value > self.threshold:
                    new_state = (new_value, None, None)
                else:
                    next_deck = list(current_deck)
                    next_deck[peek_index] -= 1
                    new_state = (new_value, None, tuple(next_deck))
                    if math.fsum(next_deck) < 1:
                        new_state = (new_value, None, None)
                        reward = new_value
                list2return.append((new_state, 1, reward))
            # not peeked
            else:
                for i in range(len(self.cardValues)):
                    reward = 0  # bust and default reward
                    # avoiding returning states with probability = 0
                    if current_deck[i] == 0:
                        continue
                    card_value = self.cardValues[i]
                    new_value = current_value + card_value
                    prob_ = current_deck[i] * prob
                    if current_value + card_value > self.threshold:
                        new_state = (new_value, None, None)
                    else:
                        next_deck = list(current_deck)
                        next_deck[i] -= 1
                        new_state = (new_value, None, tuple(next_deck))
                        if math.fsum(next_deck) < 1:
                            new_state = (new_value, None, None)
                            reward = new_value

                    list2return.append((new_state, prob_, reward))
        else:  # action == 'Peek'
            # check if peek twice
            if peek_index is not None:
                return []
            for i in range(len(self.cardValues)):
                # avoiding returning states with probability = 0
                if current_deck[i] == 0:
                    continue
                prob_ = current_deck[i] * prob
                new_state = (current_value, i, current_deck)
                list2return.append((new_state, prob_, -self.peekCost))

        return list2return
        # END_YOUR_CODE

    def discount(self):
        return 1


############################################################
# Problem 3b

def peekingMDP():
    """
    Return an instance of BlackjackMDP where peeking is the optimal action at
    least 10% of the time.
    """
    # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
    return BlackjackMDP(cardValues=[4, 5, 10, 11], multiplicity=1, threshold=20, peekCost=1)
    # END_YOUR_CODE


############################################################
# Problem 4a: Q learning

# Performs Q-learning.  Read util.RLAlgorithm for more information.
# actions: a function that takes a state and returns a list of actions.
# discount: a number between 0 and 1, which determines the discount factor
# featureExtractor: a function that takes a state and action and returns a list of (feature name, feature value) pairs.
# explorationProb: the epsilon value indicating how frequently the policy
# returns a random action
class QLearningAlgorithm(util.RLAlgorithm):
    def __init__(self, actions, discount, featureExtractor, explorationProb=0.2):
        self.actions = actions
        self.discount = discount
        self.featureExtractor = featureExtractor
        self.explorationProb = explorationProb
        self.weights = defaultdict(float)
        self.numIters = 0

    # Return the Q function associated with the weights and features
    def getQ(self, state, action):
        score = 0
        for f, v in self.featureExtractor(state, action):
            score += self.weights[f] * v
        return score

    # This algorithm will produce an action given a state.
    # Here we use the epsilon-greedy algorithm: with probability
    # |explorationProb|, take a random action.
    def getAction(self, state):
        self.numIters += 1
        if random.random() < self.explorationProb:
            return random.choice(self.actions(state))
        else:
            return max((self.getQ(state, action), action) for action in self.actions(state))[1]

    # Call this function to get the step size to update the weights.
    def getStepSize(self):
        return 1.0 / math.sqrt(self.numIters)

    # We will call this function with (s, a, r, s'), which you should use to update |weights|.
    # Note that if s is a terminal state, then s' will be None.  Remember to check for this.
    # You should update the weights using self.getStepSize(); use
    # self.getQ() to compute the current estimate of the parameters.
    def incorporateFeedback(self, state, action, reward, newState):
        # BEGIN_YOUR_CODE (our solution is 12 lines of code, but don't worry if you deviate from this)
        alpha = self.getStepSize()
        estimate = self.getQ(state, action)
        max_next_Q = 0
        if newState is not None:
            max_next_Q = max((self.getQ(newState, action), action) for action in self.actions(newState))[0]
        for f, v in self.featureExtractor(state, action):
            self.weights[f] = self.weights[f] + alpha * (reward + self.discount * max_next_Q - estimate)
        # END_YOUR_CODE


# Return a singleton list containing indicator feature for the (state, action)
# pair.  Provides no generalization.
def identityFeatureExtractor(state, action):
    featureKey = (state, action)
    featureValue = 1
    return [(featureKey, featureValue)]


############################################################
# Problem 4b: convergence of Q-learning
# Small test case
smallMDP = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=10, peekCost=1)

# Large test case
largeMDP = BlackjackMDP(cardValues=[1, 3, 5, 8, 10], multiplicity=3, threshold=40, peekCost=1)
largeMDP.computeStates()

if __name__ == '__main__' and args.p_4b == 'small':
    rl = QLearningAlgorithm(smallMDP.actions, smallMDP.discount(),
                            identityFeatureExtractor,
                            0.2)
    simulated = util.simulate(smallMDP, rl, 30000, verbose=False)
    rl.explorationProb = 0

    # value iteration
    value = ValueIteration()
    value.solve(smallMDP)

    for key in value.pi.keys():
        print 'state:', key
        print 'valit:', value.pi[key]
        print 'RLalg:', rl.getAction(key)
        print '-------------------------'

if __name__ == '__main__' and args.p_4b == 'large':
    rl = QLearningAlgorithm(largeMDP.actions, largeMDP.discount(),
                            identityFeatureExtractor,
                            0.2)
    simulated = util.simulate(largeMDP, rl, 30000, verbose=False)
    rl.explorationProb = 0

    # value iteration
    value = ValueIteration()
    value.solve(largeMDP)

    for key in value.pi.keys():
        if value.pi[key] != rl.getAction(key):
            print 'state:', key
            print 'valit:', value.pi[key]
            print 'RLalg:', rl.getAction(key)
            print '-------------------------'

############################################################
# Problem 4c: features for Q-learning.

# You should return a list of (feature key, feature value) pairs (see
# identityFeatureExtractor()).
# Implement the following features:
# - indicator on the total and the action (1 feature).
# - indicator on the presence/absence of each card and the action (1 feature).
#       Example: if the deck is (3, 4, 0 , 2), then your indicator on the presence of each card is (1,1,0,1)
#       Only add this feature if the deck != None
# - indicator on the number of cards for each card type and the action (len(counts) features).
# Only add these features if the deck != None
def blackjackFeatureExtractor(state, action):
    total, nextCard, counts = state
    # BEGIN_YOUR_CODE (our solution is 9 lines of code, but don't worry if you deviate from this)
    list2return = []
    list2return.append(((total, action), 1))
    if counts is not None:
        list2return.append(((tuple([1 if i > 0 else 0 for i in counts]), action), 1))
        for i in range(len(counts)):
            list2return.append(((i, counts[i], action), 1))
    return list2return
    # END_YOUR_CODE


############################################################
# Problem 4d: What happens when the MDP changes underneath you?!

# Original mdp
originalMDP = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=10, peekCost=1)

# New threshold
newThresholdMDP = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=15, peekCost=1)

if __name__ == '__main__' and args.p_4d:
    # value iteration
    value = ValueIteration()
    value.solve(originalMDP)
    # simulation
    rl = util.FixedRLAlgorithm(value.pi)
    simulated = util.simulate(newThresholdMDP, rl, 30000, verbose=False)
    print sum(simulated)

    rl = QLearningAlgorithm(originalMDP.actions, originalMDP.discount(),
                            identityFeatureExtractor,
                            0.2)
    simulated = util.simulate(newThresholdMDP, rl, 30000, verbose=False)
    print sum(simulated)

    rl = QLearningAlgorithm(originalMDP.actions, originalMDP.discount(),
                            identityFeatureExtractor,
                            0)
    simulated = util.simulate(newThresholdMDP, rl, 30000, verbose=False)
    print sum(simulated)
