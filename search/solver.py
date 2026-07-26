from queue import PriorityQueue
from collections import deque

from gameModel.board import Tile
from search.node import Node

import time
import tracemalloc

def depth_first_graph_search(problem):
    tracemalloc.start()
    start_time = time.perf_counter()
    expanded_nodes = 0
    stack = [Node(problem.initial)]

    visited = set()

    while stack:

        node = stack.pop()
        if problem.goal_test(node.state):
            search_time = time.perf_counter() - start_time
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            peak_memory = peak / (1024 * 1024)
            return {
                "solution": node,
                "search_time": search_time,
                "expanded_nodes": expanded_nodes,
                "peak_memory": peak_memory,
                "moves": len(node.solution())
            }

        if node.state in visited:
            continue

        expanded_nodes += 1

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
    start_time = time.perf_counter()
    frontier = PriorityQueue()
    expanded_nodes = 0
    tracemalloc.start()
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

        expanded_nodes += 1

        explored[node.state] = cost

        if problem.goal_test(node.state):
            search_time = time.perf_counter() - start_time
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            peak_memory = peak / (1024 * 1024)
            return {
                "solution": node,
                "search_time": search_time,
                "expanded_nodes": expanded_nodes,
                "peak_memory": peak_memory,
                "moves": len(node.solution())
            }

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
    start_time = time.perf_counter()
    frontier = deque([Node(problem.initial)])
    explored = set()
    expanded_nodes = 0
    tracemalloc.start()
    while frontier:
        node = frontier.popleft()
        if problem.goal_test(node.state):
            search_time = time.perf_counter() - start_time
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            peak_memory = peak / (1024 * 1024)
            return {
                "solution": node,
                "search_time": search_time,
                "expanded_nodes": expanded_nodes,
                "peak_memory": peak_memory,
                "moves": len(node.solution())
            }

        if node.state in explored:
            continue

        expanded_nodes += 1
        
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
    start_time = time.perf_counter()
    frontier = PriorityQueue()
    frontier.put((0, Node(problem.initial)))
    explored = {}
    expanded_nodes = 0
    tracemalloc.start()
    while not frontier.empty():
        priority, node = frontier.get()
        if node.state in explored and explored[node.state] <= priority:
            continue

        expanded_nodes += 1

        explored[node.state] = priority

        if problem.goal_test(node.state):
            search_time = time.perf_counter() - start_time
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            peak_memory = peak / (1024 * 1024)
            return {
                "solution": node,
                "search_time": search_time,
                "expanded_nodes": expanded_nodes,
                "peak_memory": peak_memory,
                "moves": len(node.solution())
            }

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
