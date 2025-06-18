def is_connected(graph):
    visited = set()

    def dfs(u):
        for v in graph[u]:
            if v not in visited:
                visited.add(v)
                dfs(v)

    dfs(0)
    return len(visited) == len(graph)
