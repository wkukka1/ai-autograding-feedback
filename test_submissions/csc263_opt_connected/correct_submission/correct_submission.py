from collections import deque
from typing import List


def is_connected(graph: List[List[int]]) -> bool:
    if not graph:
        return True

    num_nodes = len(graph)
    visited_nodes = [False] * num_nodes
    traversal_queue = deque([0])
    visited_nodes[0] = True
    reachable_count = 1

    while traversal_queue:
        current_node = traversal_queue.popleft()
        for neighbor_node in graph[current_node]:
            if not visited_nodes[neighbor_node]:
                visited_nodes[neighbor_node] = True
                reachable_count += 1
                traversal_queue.append(neighbor_node)

    return reachable_count == num_nodes
