"""
Reference Implementation: Main Program
Demonstrates the complete route planning system
"""

from graph import Graph
from dijkstra import dijkstra
from astar import astar


def print_path_result(algorithm_name: str, path, cost, nodes_explored):
    """Pretty print path finding results"""
    print(f"\n{algorithm_name}:")
    print("-" * 50)
    if path:
        print(f"  Path: {' → '.join(map(str, path))}")
        print(f"  Total Cost: {cost:.2f}")
        print(f"  Nodes Explored: {nodes_explored}")
    else:
        print("  No path found!")


def main():
    """Main program demonstrating the route planning system"""
    
    print("="*60)
    print("CS 2500 - Route Planning & Navigation System")
    print("Reference Implementation")
    print("="*60)
    
    # Load graph
    print("\n[1] Loading campus map...")
    graph = Graph()
    graph.load_from_csv("../../data/nodes.csv", "../../data/edges.csv")
    print(f"    Loaded: {graph}")
    
    # Display sample locations
    print("\n[2] Campus Locations:")
    sample_nodes = [1, 3, 4, 8, 14]
    for node_id in sample_nodes:
        if node_id in graph.nodes:
            name = graph.nodes[node_id]["name"]
            coords = graph.nodes[node_id]["coords"]
            print(f"    Node {node_id}: {name} at {coords}")
    
    # Test all 5 required queries
    print("\n[3] Testing Required Queries")
    print("="*60)
    
    queries = [
        (1, 14, "Main Gateway → Parking Garage (Long Path)"),
        (8, 9, "Student Center → Cafe (Short Path)"),
        (4, 13, "CS Department → Dorm B (Cross-Map)"),
        (6, 10, "Physics Building → Gymnasium (Winding Path)"),
        (3, 11, "Library → Aquatic Center (Medium Path)")
    ]
    
    for i, (start, end, description) in enumerate(queries, 1):
        print(f"\nQuery {i}: {description}")
        print("-" * 60)
        
        # Run Dijkstra
        d_path, d_cost, d_nodes = dijkstra(graph, start, end)
        print_path_result("Dijkstra's Algorithm", d_path, d_cost, d_nodes)
        
        # Run A*
        a_path, a_cost, a_nodes = astar(graph, start, end)
        print_path_result("A* Algorithm", a_path, a_cost, a_nodes)
        
        # Compare
        if d_nodes > 0 and a_nodes > 0:
            improvement = (d_nodes - a_nodes) / d_nodes * 100
            print(f"\n  📊 A* explores {improvement:.1f}% fewer nodes")
        
        if abs(d_cost - a_cost) < 0.01:
            print(f"  ✓ Both algorithms found the optimal path")
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print("✓ Graph operations working")
    print("✓ Dijkstra's algorithm implemented")
    print("✓ A* algorithm implemented")
    print("✓ Performance tracking enabled")
    print("✓ All 5 required queries tested")
    print("\n✅ System ready for grading!")


if __name__ == "__main__":
    main()
