__author__ = 'Clayton'


class Graph(object):
    """
    A simple undirected, weighted graph
    """

    def __init__(self):
        self.nodes = set()
        self.edges = {}
        self.distances = {}

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, distance):
        self._add_edge(from_node, to_node, distance)
        self._add_edge(to_node, from_node, distance)

    def _add_edge(self, from_node, to_node, distance):
        self.edges.setdefault(from_node, [])
        self.edges[from_node].append(to_node)
        self.distances[(from_node, to_node)] = distance


def astar(graph, initial_node, goal_node, h):
    closed_set = set()  # set of nodes already evaluated
    nodes = set()  # set of tentative nodes to be evaluated
    nodes.add(initial_node)

    visited = {}  # map of navigated nodes
    g_score = {initial_node: 0}  # distance from start along optimal path
    h_score = {initial_node: h(initial_node, goal_node)}  # heuristic estimate
    f_score = {initial_node: h_score[initial_node]}  # estimated distance

    while nodes:  # We pull all nodes in the 'Open Set', nodes that have not been visited
        current = None
        for node in nodes:  # Check all nodes for the lowest f_score node (best path)
            if current is None:
                current = node  # first iteration through this loop will set current to the first node
            elif f_score[node] < f_score[current]:  # We compare previous node to the next node and current becomes the smaller of the two
                current = node

        # At this point we have the smallest f_score node (best combined choice of h_score and g_score) in current
        nodes.remove(current)  # Remove node current from the open_set of unvisited nodes
        if current == goal_node:  # if current is our goal node we return the set of visited nodes, we are done!
            return visited

        closed_set.add(current)  # Add current to the set of closed nodes
        for neighbor in graph.edges[current]:  # Now we check all neighbors of current
            if neighbor in closed_set:  # if neighbor is visited (in closed set) we ignore it and continue
                continue
            tentative_g_score = g_score[current] + graph.distances[(current, neighbor)]
            # Calculate g_score (distance known from start to current to this neighbor
            # If neighbor isn't in the set of Nodes to be evaluated or if it is and this path is lower we add
            # this neighbor to be evaluated
            if neighbor not in nodes or tentative_g_score < g_score[neighbor]:
                nodes.add(neighbor)
                # add all scoring information about this neighbor so we can determine whether it is optimal
                # later on
                visited[neighbor] = current
                g_score[neighbor] = tentative_g_score
                h_score[neighbor] = h(neighbor, goal_node)
                f_score[neighbor] = g_score[neighbor] + h_score[neighbor]
    return False  # Cannot move from start to goal if we return False


def shortest_path(graph, initial_node, goal_node, h):
    paths = astar(graph, initial_node, goal_node, h)  # Returns route taken from astar algorithm
    route = [goal_node]

    while goal_node != initial_node:  # Route becomes an array of all Nodes used in the path
        route.append(paths[goal_node])  # Reverse iterate from goal to start
        goal_node = paths[goal_node]

    route.reverse()  # reverse this list so that we are going from start to goal
    return route


if __name__ == '__main__':
    import math
    # Used Euclidean distance heuristic, slower but a bit more accurate
    sldist = lambda c1, c2: math.sqrt((c2[0] - c1[0])**2 + (c2[1] - c1[1])**2)
    g = Graph()
    # here we set up the graph we are using for testing purposes
    g.add_node((0, 0))
    g.add_node((1, 1))
    g.add_node((1, 0))
    g.add_node((0, 1))
    g.add_node((2, 2))

    g.add_edge((0, 0), (1, 1), 1.5)
    g.add_edge((0, 0), (0, 1), 1.2)
    g.add_edge((0, 0), (1, 0), 1)
    g.add_edge((1, 0), (2, 2), 2)
    g.add_edge((0, 1), (2, 2), 2)
    g.add_edge((1, 1), (2, 2), 1.5)

    assert shortest_path(g, (0, 0), (2, 2), sldist) == [(0, 0), (1, 1), (2, 2)]

    g.distances[((0, 0), (1, 1))] = 2
    g.distances[((1, 1), (0, 0))] = 2

    assert shortest_path(g, (0, 0), (2, 2), sldist) == [(0, 0), (1, 0), (2, 2)]

    g.distances[((0, 0), (1, 0))] = 1.3
    g.distances[((1, 0), (0, 0))] = 1.3

    assert shortest_path(g, (0, 0), (2, 2), sldist) == [(0, 0), (0, 1), (2, 2)]


