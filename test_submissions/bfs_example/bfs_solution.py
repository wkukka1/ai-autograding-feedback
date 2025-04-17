from collections import deque


def bfs_corrected(graph, start):
    visited = set()
    queue = deque([start])

    while queue:
        node = queue.popleft()

        if node not in visited:
            visited.add(node)
            print(node, end=" ")

            for neighbor in graph[node]:
                if neighbor not in visited:
                    queue.append(neighbor)
