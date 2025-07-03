"""
The complete graph Kn is the undirected graph on n vertices in which every pair of vertices is joined
by an edge. The running time of the breadth first search algorithm discussed in class is in Θ(n2) when
the input graph is Kn.

Modify BFS to obtain an algorithm which, given an undirected graph G with n vertices and m
edges, determines whether it is connected in O(m + n) time, but whose running time for Kn is
only Θ(n). Provide implementations of your modifications to the BFS algorithm,
and explain where in the algorithm these modifications should happen.

Note: Empty graphs are considered connected
"""


def is_connected(graph):
    n = len(graph)  # Number of nodes
    visited = [False] * n
    queue = [0]
    visited[0] = True
    count = 1

    while queue:
        u = queue.pop(0)
        for v in graph[u]:  # graph is an adjacency list
            if not visited[v]:
                visited[v] = True
                queue.append(v)
                count += 1

    return count == n  # True if all nodes are reachable
