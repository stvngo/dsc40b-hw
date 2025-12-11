"""A simple implementation of a Disjoint Set Forest in Python."""
class DisjointSetForest:

    def __init__(self, elements):
        self._core = _DisjointSetForestCore()

        self.element_to_id = {}
        self.id_to_element = {}

        for element in elements:
            eid = self._core.make_set()
            self.element_to_id[element] = eid
            self.id_to_element[eid] = element

    def find_set(self, element):
        """Finds the "representative" of the set containing the element.
        Initially, each element is in its own set, and so it's representative is itself.
        Two elements which are in the same set are guaranteed to have the same
        representative.
        Example
        -------
        >>> dsf = DisjointSetForest(['a', 'b', 'c'])
        >>> dsf.find_set('a')
        'a'
        """
        return self.id_to_element[
                self._core.find_set(
                    self.element_to_id[element]
                )
            ]

    def union(self, x, y):
        """Unions the set containing `x` with the set containing `y`.
        Example
        -------
        >>> dsf = DisjointSetForest(['a', 'b', 'c'])
        >>> dsf.in_same_set('a', 'b')
        False
        >>> dsf.union('a', 'b')
        >>> dsf.in_same_set('a', 'b')
        True
        """
        x_id = self.element_to_id[x]
        y_id = self.element_to_id[y]
        self._core.union(x_id, y_id)


    def in_same_set(self, x, y):
        """Determines if elements x and y are in the same set.
        Example
        -------
        >>> dsf = DisjointSetForest(['a', 'b', 'c'])
        >>> dsf.in_same_set('a', 'b')
        False
        >>> dsf.union('a', 'b')
        >>> dsf.in_same_set('a', 'b')
        True
        """
        return self.find_set(x) == self.find_set(y)


class _DisjointSetForestCore:

    def __init__(self):
        self._parent = []
        self._rank = []
        self._size_of_set = []

    def make_set(self):
        # get the new element's "id"
        x = len(self._parent)
        self._parent.append(None)
        self._rank.append(0)
        self._size_of_set.append(1)
        return x

    def find_set(self, x):
        try:
            parent = self._parent[x]
        except IndexError:
            raise ValueError(f'{x} is not in the collection.')

        if self._parent[x] is None:
            return x
        else:
            root = self.find_set(self._parent[x])
            self._parent[x] = root
            return root

    def union(self, x, y):
        x_rep = self.find_set(x)
        y_rep = self.find_set(y)

        if x_rep == y_rep:
            return

        if self._rank[x_rep] > self._rank[y_rep]:
            self._parent[y_rep] = x_rep
            self._size_of_set[x_rep] += self._size_of_set[y_rep]
        else:
            self._parent[x_rep] = y_rep
            self._size_of_set[y_rep] += self._size_of_set[x_rep]
            if self._rank[x_rep] == self._rank[y_rep]:
                self._rank[y_rep] += 1


def test_slc():
    import dsc40graph
    g = dsc40graph.UndirectedGraph()
    edges = [('a', 'b'), ('a', 'c'), ('c', 'd'), ('b', 'd')]
    for edge in edges: g.add_edge(*edge)
    def d(edge):
        u, v = sorted(edge)
        return {
            ('a', 'b'): 1,
            ('a', 'c'): 4,
            ('b', 'd'): 3,
            ('c', 'd'): 2,
        }[(u, v)]
    print(slc(g, d, 2)) 

def slc(graph, d, k):
    # graph.nodes is an attribute, not a method
    dsf = DisjointSetForest(graph.nodes)

    # Get all edges from graph.edges (which is a view)
    # For undirected graphs, edges can be in either order, so we normalize them
    edges = []
    seen_edges = set()
    
    for edge in graph.edges:
        # Normalize edge order for undirected graph
        u, v = edge
        normalized_edge = tuple(sorted([u, v]))
        if normalized_edge not in seen_edges:
            seen_edges.add(normalized_edge)
            edges.append(normalized_edge)
    
    # Sort edges by distance (ascending order)
    edges.sort(key=lambda edge: d(edge))
    
    # Process edges until we have k clusters
    # Start with n clusters (one per vertex)
    num_clusters = len(graph.nodes)
    
    for edge in edges:
        # If we already have k clusters, we're done
        if num_clusters == k:
            break
            
        u, v = edge
        # If u and v are in different clusters, merge them
        if not dsf.in_same_set(u, v):
            dsf.union(u, v)
            num_clusters -= 1
    
    # Build the result: group vertices by their cluster representative
    clusters = {}
    for vertex in graph.nodes:
        rep = dsf.find_set(vertex)
        if rep not in clusters:
            clusters[rep] = set()
        clusters[rep].add(vertex)
    
    # Return as frozenset of frozensets
    return frozenset(frozenset(cluster) for cluster in clusters.values())

if __name__ == "__main__":
    test_slc()