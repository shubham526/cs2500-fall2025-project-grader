"""
Reference Implementation: Graph Class
This is a working implementation you can use to test the autograder
and calculate expected optimal costs for the test queries.
"""

import csv
from typing import Dict, List, Tuple, Optional


class Graph:
    """Graph data structure for route planning"""

    def __init__(self):
        self.nodes: Dict[int, dict] = {}  # node_id -> {"name": str, "coords": (x, y)}
        self.edges: Dict[int, Dict[int, float]] = {}  # from_id -> {to_id: weight}

    def load_from_csv(self, nodes_file: str, edges_file: str):
        """Load graph data from CSV files"""
        # Load nodes
        with open(nodes_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                node_id = int(row['id'])
                name = row['name']
                x = float(row['x'])
                y = float(row['y'])
                self.add_node(node_id, name, (x, y))

        # Load edges
        with open(edges_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                from_node = int(row['from'])
                to_node = int(row['to'])
                weight = float(row['weight'])
                self.add_edge(from_node, to_node, weight)

    def add_node(self, node_id: int, name: str, coords: Tuple[float, float]):
        """Add a node to the graph"""
        self.nodes[node_id] = {
            "name": name,
            "coords": coords
        }
        if node_id not in self.edges:
            self.edges[node_id] = {}

    def remove_node(self, node_id: int):
        """Remove a node from the graph"""
        if node_id in self.nodes:
            del self.nodes[node_id]

        if node_id in self.edges:
            del self.edges[node_id]

        # Remove edges pointing to this node
        for neighbors in self.edges.values():
            if node_id in neighbors:
                del neighbors[node_id]

    def add_edge(self, from_id: int, to_id: int, weight: float):
        """Add an edge to the graph"""
        if from_id not in self.edges:
            self.edges[from_id] = {}
        self.edges[from_id][to_id] = weight

    def remove_edge(self, from_id: int, to_id: int):
        """Remove an edge from the graph"""
        if from_id in self.edges and to_id in self.edges[from_id]:
            del self.edges[from_id][to_id]

    def get_neighbors(self, node_id: int) -> List[int]:
        """Get all neighbors of a node"""
        return list(self.edges.get(node_id, {}).keys())

    def get_edge_weight(self, from_id: int, to_id: int) -> Optional[float]:
        """Get the weight of an edge"""
        return self.edges.get(from_id, {}).get(to_id)

    def get_node_coords(self, node_id: int) -> Optional[Tuple[float, float]]:
        """Get coordinates of a node"""
        node_data = self.nodes.get(node_id)
        return node_data["coords"] if node_data else None

    def has_node(self, node_id: int) -> bool:
        """Check if node exists"""
        return node_id in self.nodes

    def has_edge(self, from_id: int, to_id: int) -> bool:
        """Check if edge exists"""
        return from_id in self.edges and to_id in self.edges[from_id]

    def num_nodes(self) -> int:
        """Get number of nodes"""
        return len(self.nodes)

    def num_edges(self) -> int:
        """Get number of edges"""
        return sum(len(neighbors) for neighbors in self.edges.values())

    def __str__(self):
        return f"Graph with {self.num_nodes()} nodes and {self.num_edges()} edges"


if __name__ == "__main__":
    # Test the graph
    g = Graph()
    g.load_from_csv("reference_data/nodes.csv", "reference_data/edges.csv")
    print(g)
    print(f"Node 1 neighbors: {g.get_neighbors(1)}")
    print(f"Edge weight 1->2: {g.get_edge_weight(1, 2)}")