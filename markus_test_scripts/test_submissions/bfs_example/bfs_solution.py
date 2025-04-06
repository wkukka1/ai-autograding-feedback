from collections import deque

def bfs_corrected(graph, start):
    visited = set()  # Set to keep track of visited nodes
    queue = deque([start])  # Queue to manage the BFS queue

    while queue:
        node = queue.popleft()  # Corrected: use popleft() instead of pop()

        if node not in visited:
            visited.add(node)
            print(node, end=" ")

            # Adding neighbors to the queue
            for neighbor in graph[node]:
                if neighbor not in visited:
                    queue.append(neighbor)
