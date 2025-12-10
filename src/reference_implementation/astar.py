"""
A* Search Algorithm - Reference Implementation
CS 2500 Extra Credit Project
"""

import heapq
from math import inf, sqrt


def heuristic(graph, node, goal):
    """
    Heuristic function: Euclidean (straight-line) distance.
    This is admissible because straight-line distance never overestimates
    the actual path distance.

    Args:
        graph: Graph object with get_node_coords() method
        node (int): Current node ID
        goal (int): Goal node ID

    Returns:
        float: Estimated distance from node to goal
    """
    x1, y1 = graph.get_node_coords(node)
    x2, y2 = graph.get_node_coords(goal)

    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def astar(graph, start, goal):
    """
    Find shortest path using A* search algorithm.

    Args:
        graph: Graph object with getNeighbors(node_id) and get_node_coords(node_id) methods
        start (int): Starting node ID
        goal (int): Goal node ID

    Returns:
        dict: Dictionary containing:
            - 'path': List of node IDs in the shortest path
            - 'cost': Total cost of the shortest path
            - 'nodes_explored': Number of nodes explored
    """
    # g(n): actual cost from start to n
    g = {node_id: inf for node_id in graph.nodes}
    g[start] = 0

    # f(n) = g(n) + h(n): estimated total cost
    f = {node_id: inf for node_id in graph.nodes}
    f[start] = heuristic(graph, start, goal)

    # Track previous nodes for path reconstruction
    prev = {node_id: None for node_id in graph.nodes}

    # Priority queue: (f_score, node_id)
    pq = [(f[start], start)]

    # Track visited nodes
    visited = set()
    nodes_explored = 0

    while pq:
        current_f, u = heapq.heappop(pq)

        # Skip if already visited
        if u in visited:
            continue

        visited.add(u)
        nodes_explored += 1

        # Check if we reached the goal
        if u == goal:
            break

        # Explore neighbors
        for neighbor, weight in graph.getNeighbors(u):
            tentative_g = g[u] + weight

            if tentative_g < g[neighbor]:
                # This path to neighbor is better
                g[neighbor] = tentative_g
                f[neighbor] = tentative_g + heuristic(graph, neighbor, goal)
                prev[neighbor] = u
                heapq.heappush(pq, (f[neighbor], neighbor))

    # Check if path exists
    if g[goal] == inf:
        return {
            'path': [],
            'cost': inf,
            'nodes_explored': nodes_explored
        }

    # Reconstruct path
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = prev[current]
    path.reverse()

    return {
        'path': path,
        'cost': g[goal],
        'nodes_explored': nodes_explored
    }


if __name__ == "__main__":
    """Test A* algorithm"""
    from graph import Graph

    # Load graph
    g = Graph()
    g.load_from_csv("../../data/nodes.csv", "../../data/edges.csv")

    print("Testing A* Search Algorithm")
    print("=" * 60)
    print(f"Graph loaded: {g.num_nodes()} nodes, {g.num_edges()} edges\n")

    # Required test queries
    queries = [
        (1, 14),  # Main Gateway → Parking Garage (Long Path)
        (8, 9),  # Student Center → Cafe (Short Path)
        (4, 13),  # CS Department → Dorm B (Cross-Map)
        (6, 10),  # Physics Building → Gymnasium (Winding Path)
        (3, 11),  # Library → Aquatic Center (Medium Path)
    ]

    # Test each query
    for start, goal in queries:
        result = astar(g, start, goal)

        print(f"Query: {start} → {goal}")
        print(f"  Path: {' → '.join(map(str, result['path']))}")
        print(f"  Cost: {result['cost']}")
        print(f"  Nodes explored: {result['nodes_explored']}")
        print()