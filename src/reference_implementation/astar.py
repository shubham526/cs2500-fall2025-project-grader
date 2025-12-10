"""
Reference Implementation: A* Algorithm
This is a working implementation you can use to test the autograder.
"""

import heapq
import math
from typing import List, Tuple, Optional


def euclidean_distance(coords1: Tuple[float, float], coords2: Tuple[float, float]) -> float:
    """Calculate Euclidean distance between two points"""
    x1, y1 = coords1
    x2, y2 = coords2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def astar(graph, start: int, end: int) -> Tuple[List[int], float, int]:
    """
    Find shortest path using A* algorithm
    
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
    # Get end coordinates for heuristic
    end_coords = graph.get_node_coords(end)
    if end_coords is None:
        return None, float('infinity'), 0
    
    # g(n): actual cost from start to n
    g_scores = {node: float('infinity') for node in graph.nodes}
    g_scores[start] = 0
    
    # f(n) = g(n) + h(n): estimated total cost
    # h(n): heuristic (Euclidean distance to goal)
    def heuristic(node_id: int) -> float:
        """Admissible heuristic: straight-line distance to goal"""
        node_coords = graph.get_node_coords(node_id)
        if node_coords is None:
            return 0
        return euclidean_distance(node_coords, end_coords)
    
    # Priority queue: (f_score, node_id)
    # f_score = g_score + heuristic
    start_h = heuristic(start)
    pq = [(start_h, start)]
    
    # Track previous nodes for path reconstruction
    previous = {node: None for node in graph.nodes}
    
    # Visited nodes
    visited = set()
    nodes_explored = 0
    
    while pq:
        current_f, current_node = heapq.heappop(pq)
        
        # Skip if already visited
        if current_node in visited:
            continue
        
        visited.add(current_node)
        nodes_explored += 1
        
        # Found the destination
        if current_node == end:
            break
        
        # Explore neighbors
        for neighbor in graph.get_neighbors(current_node):
            if neighbor in visited:
                continue
            
            edge_weight = graph.get_edge_weight(current_node, neighbor)
            if edge_weight is None:
                continue
            
            # Calculate tentative g_score
            tentative_g = g_scores[current_node] + edge_weight
            
            # Found a better path to neighbor
            if tentative_g < g_scores[neighbor]:
                g_scores[neighbor] = tentative_g
                previous[neighbor] = current_node
                
                # f(n) = g(n) + h(n)
                f_score = tentative_g + heuristic(neighbor)
                heapq.heappush(pq, (f_score, neighbor))
    
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
    
    return path, g_scores[end], nodes_explored


if __name__ == "__main__":
    # Test A* algorithm
    import sys
    sys.path.append('..')
    from graph import Graph
    from dijkstra import dijkstra
    
    g = Graph()
    g.load_from_csv("../../data/nodes.csv", "../../data/edges.csv")
    
    print("Testing A* Algorithm")
    print("="*60)
    
    # Test queries
    queries = [
        (1, 14, "Main Gateway → Parking Garage"),
        (8, 9, "Student Center → Cafe"),
        (4, 13, "CS Department → Dorm B"),
        (6, 10, "Physics Building → Gymnasium"),
        (3, 11, "Library → Aquatic Center")
    ]
    
    print("\nComparison: Dijkstra vs A*")
    print("-"*60)
    
    for start, end, description in queries:
        # Run Dijkstra
        d_path, d_cost, d_nodes = dijkstra(g, start, end)
        
        # Run A*
        a_path, a_cost, a_nodes = astar(g, start, end)
        
        print(f"\n{description}")
        print(f"  Dijkstra: cost={d_cost:.1f}, nodes={d_nodes}")
        print(f"  A*:       cost={a_cost:.1f}, nodes={a_nodes}")
        
        # Calculate improvement
        if d_nodes > 0:
            improvement = (d_nodes - a_nodes) / d_nodes * 100
            print(f"  A* explores {improvement:.1f}% fewer nodes")
        
        # Verify both find same optimal cost
        if abs(d_cost - a_cost) < 0.01:
            print(f"  ✓ Both found optimal path")
        else:
            print(f"  ✗ WARNING: Costs differ!")
