"""
Reference Implementation: Dijkstra's Algorithm
This is a working implementation you can use to test the autograder
and calculate expected optimal costs.
"""

import heapq
from typing import List, Tuple, Optional, Dict


def dijkstra(graph, start: int, end: int) -> Tuple[List[int], float, int]:
    """
    Find shortest path using Dijkstra's algorithm
    
    Args:
        graph: Graph instance
        start: Starting node ID
        end: Ending node ID
    
    Returns:
        (path, cost, nodes_explored): 
            - path: List of node IDs from start to end
            - cost: Total cost of the path
            - nodes_explored: Number of nodes examined
    """
    # Initialize
    distances = {node: float('infinity') for node in graph.nodes}
    distances[start] = 0
    
    previous = {node: None for node in graph.nodes}
    
    # Priority queue: (distance, node_id)
    pq = [(0, start)]
    
    visited = set()
    nodes_explored = 0
    
    while pq:
        current_dist, current_node = heapq.heappop(pq)
        
        # Skip if already visited
        if current_node in visited:
            continue
        
        visited.add(current_node)
        nodes_explored += 1
        
        # Found the destination
        if current_node == end:
            break
        
        # Check if current distance is outdated
        if current_dist > distances[current_node]:
            continue
        
        # Explore neighbors
        for neighbor in graph.get_neighbors(current_node):
            edge_weight = graph.get_edge_weight(current_node, neighbor)
            
            if edge_weight is None:
                continue
            
            distance = current_dist + edge_weight
            
            # Found a shorter path to neighbor
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))
    
    # Reconstruct path
    path = []
    current = end
    
    if previous[current] is None and current != start:
        # No path exists
        return None, float('infinity'), nodes_explored
    
    while current is not None:
        path.append(current)
        current = previous[current]
    
    path.reverse()
    
    return path, distances[end], nodes_explored


def calculate_expected_costs(graph):
    """
    Calculate expected costs for all required test queries
    Use this to update EXPECTED_COSTS in test_suite.py
    """
    # Required queries from project spec
    queries = [
        (1, 14, "Main Gateway → Parking Garage (Long Path)"),
        (8, 9, "Student Center → Cafe (Short Path)"),
        (4, 13, "CS Department → Dorm B (Cross-Map)"),
        (6, 10, "Physics Building → Gymnasium (Winding Path)"),
        (3, 11, "Library → Aquatic Center (Medium Path)")
    ]
    
    print("EXPECTED COSTS FOR TEST QUERIES:")
    print("="*60)
    print("Copy these values to test_suite.py -> EXPECTED_COSTS\n")
    
    print("EXPECTED_COSTS = {")
    for start, end, description in queries:
        path, cost, nodes = dijkstra(graph, start, end)
        print(f"    ({start}, {end}): {cost},  # {description}")
        print(f"    #   Path: {' → '.join(map(str, path))}")
        print(f"    #   Nodes explored: {nodes}\n")
    print("}")


if __name__ == "__main__":
    # Test Dijkstra's algorithm and calculate expected costs
    import sys
    sys.path.append('..')
    from graph import Graph
    
    g = Graph()
    g.load_from_csv("../../data/nodes.csv", "../../data/edges.csv")
    
    print("Testing Dijkstra's Algorithm")
    print("="*60)
    
    # Test a simple query
    path, cost, nodes = dijkstra(g, 1, 14)
    print(f"\nQuery: 1 → 14")
    print(f"Path: {' → '.join(map(str, path))}")
    print(f"Cost: {cost}")
    print(f"Nodes explored: {nodes}")
    
    print("\n")
    
    # Calculate all expected costs
    calculate_expected_costs(g)
