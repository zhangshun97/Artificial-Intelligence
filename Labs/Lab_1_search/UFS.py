#! python3
# a stack for search
# Sean, Mar 2018

import heapq


class PriorityQueue(object):
    def __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (priority, _, item) = heapq.heappop(self.heap)
        return priority, item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)


class node:
    """define node"""

    def __init__(self, state, parent, path_cost, action):
        self.state = state
        self.parent = parent
        self.path_cost = path_cost
        self.action = action


class problem:
    """searching problem"""

    def __init__(self, initial_state, actions):
        self.initial_state = initial_state
        self.actions = actions
        # 可以在这里随意添加代码或者不加

    def search_actions(self, state):
        try:
            out = self.actions[state]
        except KeyError:
            out = []

        return out

    def solution(self, node):
        position = node
        path = ['Start']
        while position.state != self.initial_state:
            path.insert(1, position.state)
            position = position.parent
        return path

    def transition(self, state, action):
        return action[1]

    def goal_test(self, state):
        # default the goal is 'Goal'
        return state == 'Goal'

    def step_cost(self, state1, action, state2):
        return int(action[-1])

    def child_node(self, node_begin, action):
        child = node(state=action[1],
                     parent=node_begin,
                     path_cost=int(action[-1]),
                     action=self.actions[action[0]])
        return child


def UCS(problem):
    node_initial = node(problem.initial_state, '', 0, '')
    frontier = PriorityQueue()
    frontier.push(node_initial, node_initial.path_cost)
    explored = set()
    while not frontier.isEmpty():
        c_priority, current_node = frontier.pop()  # choose the cheapest path

        if problem.goal_test(current_node.state):
            return problem.solution(current_node)

        explored.add(current_node.state)

        potential_list = problem.search_actions(current_node.state)

        for action in potential_list:
            child = problem.child_node(current_node, action)
            if child.state not in explored:
                priority = child.path_cost + c_priority
                frontier.update(child, priority=priority)

    return 'Unreachable'


def main():
    actions = {}  # to be a diction
    # print('Enter the graph:')
    while True:
        a = input().strip()

        if a != 'END':
            a = a.split()
            try:
                actions[a[0]].append(a)
            except KeyError:
                actions[a[0]] = [a]
        else:
            break

    if not len(actions):
        print('Unreachable')
        return

    graph_problem = problem('Start', actions)
    answer = UCS(graph_problem)
    s = "->"
    if answer == 'Unreachable':
        print(answer)
    else:
        path = s.join(answer)
        print(path)


if __name__ == '__main__':
    main()
