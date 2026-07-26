class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):

        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __lt__(self, other):
        return self.path_cost < other.path_cost

    def solution(self):
        actions = []
        node = self

        while node.parent is not None:
            actions.append(node.action)
            node = node.parent

        actions.reverse()
        return actions

    def path(self):
        nodes = []
        node = self

        while node is not None:
            nodes.append(node)
            node = node.parent

        nodes.reverse()
        return nodes