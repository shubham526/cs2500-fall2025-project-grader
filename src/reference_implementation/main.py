"""
Main Program - Reference Implementation
CS 2500 Extra Credit Project
Demonstrates graph operations, Dijkstra's algorithm, and A* search
"""

from graph import Graph
from dijkstra import dijkstra
from astar import astar
import time


def main():
    """Main program demonstrating all functionality"""

    # Load graph from CSV files
    print("Loading graph from CSV files...")
    g = Graph()
    g.load_from_csv("../../data/nodes.csv", "../../data/edges.csv")

    print(f"Graph loaded successfully!")
    print(f"  Nodes: {g.num_nodes()}")
    print(f"  Edges: {g.num_edges()}")
    print()

    # Required test queries from project spec (Section 2.4.2)
    queries = [
        (1, 14),  # Query 1: Main Gateway → Parking Garage (Long Path)
        (8, 9),  # Query 2: Student Center → Cafe (Short Path)
        (4, 13),  # Query 3: CS Department → Dorm B (Cross-Map)
        (6, 10),  # Query 4: Physics Building → Gymnasium (Winding Path)
        (3, 11),  # Query 5: Library → Aquatic Center (Medium Path)
    ]

    print("Running required path queries...")
    print("=" * 70)
    print()

    # Test each query with both algorithms
    for i, (start, goal) in enumerate(queries, 1):
        start_name = g.get_node_name(start)
        goal_name = g.get_node_name(goal)

        print(f"Query {i}: {start_name} (Node {start}) → {goal_name} (Node {goal})")
        print("-" * 70)

        # Run Dijkstra
        t0 = time.perf_counter()
        dijkstra_result = dijkstra(g, start, goal)
        t1 = time.perf_counter()
        dijkstra_time = (t1 - t0) * 1000  # Convert to milliseconds

        # Run A*
        t0 = time.perf_counter()
        astar_result = astar(g, start, goal)
        t1 = time.perf_counter()
        astar_time = (t1 - t0) * 1000  # Convert to milliseconds

        # Display Dijkstra results
        print("  Dijkstra's Algorithm:")
        print(f"    Path: {' → '.join(map(str, dijkstra_result['path']))}")
        print(f"    Cost: {dijkstra_result['cost']:.2f}")
        print(f"    Nodes explored: {dijkstra_result['nodes_explored']}")
        print(f"    Time: {dijkstra_time:.4f} ms")

        # Display A* results
        print("  A* Search:")
        print(f"    Path: {' → '.join(map(str, astar_result['path']))}")
        print(f"    Cost: {astar_result['cost']:.2f}")
        print(f"    Nodes explored: {astar_result['nodes_explored']}")
        print(f"    Time: {astar_time:.4f} ms")

        # Comparison
        if dijkstra_result['cost'] == astar_result['cost']:
            print("  ✓ Both algorithms found the same optimal path")
        else:
            print("  ⚠ Warning: Algorithms found different costs!")

        # Performance improvement
        if astar_result['nodes_explored'] < dijkstra_result['nodes_explored']:
            improvement = ((dijkstra_result['nodes_explored'] - astar_result['nodes_explored']) /
                           dijkstra_result['nodes_explored'] * 100)
            print(f"  A* explored {improvement:.1f}% fewer nodes than Dijkstra")

        print()

    # Summary statistics
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)

    total_dijkstra_nodes = 0
    total_astar_nodes = 0

    for start, goal in queries:
        d_result = dijkstra(g, start, goal)
        a_result = astar(g, start, goal)
        total_dijkstra_nodes += d_result['nodes_explored']
        total_astar_nodes += a_result['nodes_explored']

    print(f"Total nodes explored across all queries:")
    print(f"  Dijkstra: {total_dijkstra_nodes}")
    print(f"  A*: {total_astar_nodes}")

    if total_astar_nodes < total_dijkstra_nodes:
        improvement = ((total_dijkstra_nodes - total_astar_nodes) / total_dijkstra_nodes * 100)
        print(f"  A* Improvement: {improvement:.1f}% fewer nodes explored")

    print()
    print("All required queries completed successfully!")


if __name__ == "__main__":
    main()