from queue import PriorityQueue

from search.node import Node


def depth_first_graph_search(problem):

    stack = [Node(problem.initial)]

    visited = set()

    while stack:

        node = stack.pop()

        if problem.goal_test(node.state):
            return node

        if node.state in visited:
            continue

        visited.add(node.state)

        for action in reversed(problem.actions(node.state)):

            childState = problem.result(
                node.state,
                action
            )

            if childState is None:
                continue

            if childState in visited:
                continue

            child = Node(
                childState,
                parent=node,
                action=action,
                path_cost=node.path_cost + 1
            )

            stack.append(child)

    return None


def uniform_cost_search(problem):

    frontier = PriorityQueue()

    frontier.put(
        (
            0,
            Node(problem.initial)
        )
    )

    explored = {}

    while not frontier.empty():

        cost, node = frontier.get()

        if (
            node.state in explored
            and explored[node.state] <= cost
        ):
            continue

        explored[node.state] = cost

        if problem.goal_test(node.state):
            return node

        for action in problem.actions(node.state):

            childState = problem.result(
                node.state,
                action
            )

            if childState is None:
                continue

            step = problem.step_cost(
                node.state,
                action,
                childState
            )

            total = node.path_cost + step

            if (
                childState in explored
                and explored[childState] <= total
            ):
                continue

            child = Node(
                childState,
                parent=node,
                action=action,
                path_cost=total
            )

            frontier.put(
                (
                    total,
                    child
                )
            )

    return None