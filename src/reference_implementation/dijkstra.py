"""
Dijkstra's Algorithm - Reference Implementation
CS 2500 Extra Credit Project
"""

import heapq
from math import inf


def dijkstra(graph, start, goal):
    """
    Find shortest path using Dijkstra's algorithm.

    Args:
        graph: Graph object with getNeighbors(node_id) method
        start (int): Starting node ID
        goal (int): Goal node ID

    Returns:
        dict: Dictionary containing:
            - 'path': List of node IDs in the shortest path
            - 'cost': Total cost of the shortest path
            - 'nodes_explored': Number of nodes explored
    """
    # Initialize distances
    dist = {node_id: inf for node_id in graph.nodes}
    dist[start] = 0

    # Track previous nodes for path reconstruction
    prev = {node_id: None for node_id in graph.nodes}

    # Priority queue: (distance, node_id)
    pq = [(0, start)]

    # Track visited nodes
    visited = set()
    nodes_explored = 0

    while pq:
        current_dist, u = heapq.heappop(pq)

        # Skip if already visited
        if u in visited:
            continue

        visited.add(u)
        nodes_explored += 1

        # Early exit if we reached the goal
        if u == goal:
            break

        # Explore neighbors
        for neighbor, weight in graph.getNeighbors(u):
            if neighbor in visited:
                continue

            new_dist = current_dist + weight

            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                prev[neighbor] = u
                heapq.heappush(pq, (new_dist, neighbor))

    # Check if path exists
    if dist[goal] == inf:
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
        'cost': dist[goal],
        'nodes_explored': nodes_explored
    }


def calculate_expected_costs(graph, queries):
    """
    Calculate expected costs for test queries.
    Use this to generate EXPECTED_COSTS for test_suite.py

    Args:
        graph: Graph object
        queries: List of (start, goal) tuples

    Returns:
        dict: Dictionary mapping (start, goal) to cost
    """
    print("\nEXPECTED COSTS FOR TEST QUERIES:")
    print("=" * 60)
    print("Copy these values to test_suite.py -> EXPECTED_COSTS\n")
    print("EXPECTED_COSTS = {")

    expected_costs = {}

    for start, goal in queries:
        result = dijkstra(graph, start, goal)
        cost = result['cost']
        path = result['path']
        nodes_explored = result['nodes_explored']

        expected_costs[(start, goal)] = cost

        # Format with comment showing path
        path_str = " → ".join(map(str, path))
        print(f"    ({start}, {goal}): {cost},  # {graph.get_node_name(start)} → {graph.get_node_name(goal)}")
        print(f"    #   Path: {path_str}")
        print(f"    #   Nodes explored: {nodes_explored}")
        print()

    print("}")

    return expected_costs


if __name__ == "__main__":
    """Test Dijkstra's algorithm and calculate expected costs"""
    from graph import Graph

    # Load graph
    g = Graph()
    g.load_from_csv("../../data/nodes.csv", "../../data/edges.csv")

    print("Testing Dijkstra's Algorithm")
    print("=" * 60)
    print(f"Graph loaded: {g.num_nodes()} nodes, {g.num_edges()} edges\n")

    # Required test queries from project spec
    queries = [
        (1, 14),  # Main Gateway → Parking Garage (Long Path)
        (8, 9),  # Student Center → Cafe (Short Path)
        (4, 13),  # CS Department → Dorm B (Cross-Map)
        (6, 10),  # Physics Building → Gymnasium (Winding Path)
        (3, 11),  # Library → Aquatic Center (Medium Path)
    ]

    # Test each query
    for start, goal in queries:
        result = dijkstra(g, start, goal)

        print(f"Query: {start} → {goal}")
        print(f"  Path: {' → '.join(map(str, result['path']))}")
        print(f"  Cost: {result['cost']}")
        print(f"  Nodes explored: {result['nodes_explored']}")
        print()

    # Calculate expected costs for test suite
    calculate_expected_costs(g, queries)