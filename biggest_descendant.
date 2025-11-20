def biggest_descendent(graph, root, value):
    best = {}

    def dfs(u):
        m = value[u]          # include itself
        for v in graph.neighbors(u):  # children
            m = max(m, dfs(v))
        best[u] = m
        return m

    dfs(root)
    return best
