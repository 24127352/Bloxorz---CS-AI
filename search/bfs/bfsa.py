from collections import deque
from queue import PriorityQueue

from gameModel.board import Tile
from search.node import Node

def manhattan_heuristic(problem, state):
    """Return an admissible heuristic based on Manhattan distance to the goal."""
    goal_positions = []
    for r, row in enumerate(state.board.tiles):
        for c, tile in enumerate(row):
            if tile == Tile.GOAL:
                goal_positions.append((r, c))

    if not goal_positions:
        return 0

    block = state.block
    goal_r, goal_c = goal_positions[0]

    return abs(block.r - goal_r) + abs(block.c - goal_c)


def breadth_first_search(problem):
    frontier = deque([Node(problem.initial)])
    explored = set()

    while frontier:
        node = frontier.popleft()

        if problem.goal_test(node.state):
            return node

        if node.state in explored:
            continue

        explored.add(node.state)

        for action in problem.actions(node.state):
            child_state = problem.result(node.state, action)

            if child_state is None or child_state in explored:
                continue

            child = Node(
                child_state,
                parent=node,
                action=action,
                path_cost=node.path_cost + 1,
            )
            frontier.append(child)

    return None


def a_star_search(problem):
    frontier = PriorityQueue()
    frontier.put((0, Node(problem.initial)))
    explored = {}

    while not frontier.empty():
        priority, node = frontier.get()

        if node.state in explored and explored[node.state] <= priority:
            continue

        explored[node.state] = priority

        if problem.goal_test(node.state):
            return node

        for action in problem.actions(node.state):
            child_state = problem.result(node.state, action)

            if child_state is None:
                continue

            if child_state in explored:
                continue

            step_cost = problem.step_cost(node.state, action, child_state)
            total_cost = node.path_cost + step_cost
            heuristic = manhattan_heuristic(problem, child_state)

            child = Node(
                child_state,
                parent=node,
                action=action,
                path_cost=total_cost,
            )
            frontier.put((total_cost + heuristic, child))

    return None
