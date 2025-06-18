def is_connected(graph):
    visited = {}
    for i in range(len(graph)):
        visited[i] = False

    queue = []
    queue.append(0)
    visited[0] = True

    while len(queue) > 0:
        current = queue.pop(0)
        for neighbor in graph[current]:
            if visited[neighbor] == False:
                visited[neighbor] = True
                queue.append(neighbor)

    for node in visited:
        if visited[node] == False:
            return False
    return True
