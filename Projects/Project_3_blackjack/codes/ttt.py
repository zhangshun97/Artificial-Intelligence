#!/usr/bin/env python

import submission

mdp1 = submission.BlackjackMDP(cardValues=[1, 5], multiplicity=2,
                                   threshold=10, peekCost=1)
startState = mdp1.startState()
preBustState = (6, None, (1, 1))
postBustState = (11, None, None)

mdp2 = submission.BlackjackMDP(cardValues=[1, 5], multiplicity=2,
                               threshold=15, peekCost=1)
preEmptyState = (11, None, (1,0))

# Make sure the succAndProbReward function is implemented correctly.
tests = [
    ([((1, None, (1, 2)), 0.5, 0), ((5, None, (2, 1)), 0.5, 0)], mdp1, startState, 'Take'),
    ([((0, 0, (2, 2)), 0.5, -1), ((0, 1, (2, 2)), 0.5, -1)], mdp1, startState, 'Peek'),
    ([((0, None, None), 1, 0)], mdp1, startState, 'Quit'),
    ([((7, None, (0, 1)), 0.5, 0), ((11, None, None), 0.5, 0)], mdp1, preBustState, 'Take'),
    ([], mdp1, postBustState, 'Take'),
    ([], mdp1, postBustState, 'Peek'),
    ([], mdp1, postBustState, 'Quit'),
    ([((12, None, None), 1, 12)], mdp2, preEmptyState, 'Take')
]
for gold, mdp, state, action in tests:
    print state, action
    print '-'*30
    print mdp.succAndProbReward(state, action)