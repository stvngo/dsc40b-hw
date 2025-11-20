def cluster(graph, weights, level):
    seen = set()
    clusters = []

    for s in graph.nodes:
        if s in seen:
            continue

        # start a component from s
        comp = set()
        stack = [s]
        seen.add(s)

        while stack:
            u = stack.pop()
            comp.add(u)
            for v in graph.neighbors(u):
                # keep this edge only if weight >= level
                if weights(u, v) >= level and v not in seen:
                    seen.add(v)
                    stack.append(v)

        clusters.append(frozenset(comp))

    return frozenset(clusters)