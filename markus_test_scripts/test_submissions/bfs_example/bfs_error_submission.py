from collections import deque

def bfs_with_error(graph, start):
    visited = set()  # Set to keep track of visited nodes
    queue = deque([start])  # Queue to manage the BFS queue

    while queue:
        node = queue.pop()  # Error: we should use popleft(), not pop()

        if node not in visited:
            visited.add(node)
            print(node, end=" ")

            # Adding neighbors to the queue
            for neighbor in graph[node]:
                if neighbor not in visited:
                    queue.append(neighbor)
