"""
Graph Data Structure - Reference Implementation
Matches CS 2500 Extra Credit Project Specification (Section 2.1.3)
"""

import csv


class Graph:
    """
    Graph data structure for representing weighted, directed graphs.
    Supports nodes with coordinates and weighted edges.
    """

    def __init__(self):
        """Initialize empty graph"""
        # Store nodes: node_id -> (name, (x, y))
        self.nodes = {}
        # Adjacency list: node_id -> [(neighbor_id, weight), ...]
        self.adj = {}

    def addNode(self, node_id, name, coordinates):
        """
        Add a new node to the graph.

        Args:
            node_id (int): Unique identifier for the node
            name (str): Name/label for the node
            coordinates (tuple): (x, y) coordinates for A* heuristic
        """
        self.nodes[node_id] = (name, coordinates)
        if node_id not in self.adj:
            self.adj[node_id] = []

    def addEdge(self, from_node, to_node, weight):
        """
        Add a directed edge from one node to another.

        Args:
            from_node (int): Source node ID
            to_node (int): Destination node ID
            weight (float): Edge weight (distance/cost)
        """
        if from_node not in self.adj:
            self.adj[from_node] = []
        self.adj[from_node].append((to_node, weight))

    def removeNode(self, node_id):
        """
        Remove a node and all edges connected to it.

        Args:
            node_id (int): Node ID to remove
        """
        # Remove from nodes dict
        if node_id in self.nodes:
            del self.nodes[node_id]

        # Remove from adjacency list
        if node_id in self.adj:
            del self.adj[node_id]

        # Remove all incoming edges to this node
        for src in self.adj:
            self.adj[src] = [(neighbor, weight) for neighbor, weight in self.adj[src]
                             if neighbor != node_id]

    def removeEdge(self, from_node, to_node):
        """
        Remove a directed edge between two nodes.

        Args:
            from_node (int): Source node ID
            to_node (int): Destination node ID
        """
        if from_node in self.adj:
            self.adj[from_node] = [(neighbor, weight) for neighbor, weight in self.adj[from_node]
                                   if neighbor != to_node]

    def getNeighbors(self, node_id):
        """
        Get all neighbors of a node.

        Args:
            node_id (int): Node ID

        Returns:
            list: List of (neighbor_id, weight) tuples
        """
        return self.adj.get(node_id, [])

    def getEdgeWeight(self, from_node, to_node):
        """
        Get the weight of an edge between two nodes.

        Args:
            from_node (int): Source node ID
            to_node (int): Destination node ID

        Returns:
            float: Edge weight, or None if edge doesn't exist
        """
        for neighbor, weight in self.adj.get(from_node, []):
            if neighbor == to_node:
                return weight
        return None

    def load_from_csv(self, nodes_path, edges_path):
        """
        Load graph data from CSV files.

        Args:
            nodes_path (str): Path to nodes.csv file
            edges_path (str): Path to edges.csv file
        """
        # Load nodes from CSV
        with open(nodes_path, 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header
            for row in reader:
                if not row:  # Skip empty rows
                    continue
                node_id = int(row[0])
                name = row[1]
                x = float(row[2])
                y = float(row[3])
                self.addNode(node_id, name, (x, y))

        # Load edges from CSV
        with open(edges_path, 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header
            for row in reader:
                if not row:  # Skip empty rows
                    continue
                from_node = int(row[0])
                to_node = int(row[1])
                weight = float(row[2])
                self.addEdge(from_node, to_node, weight)

    def num_nodes(self):
        """Return the number of nodes in the graph"""
        return len(self.nodes)

    def num_edges(self):
        """Return the number of edges in the graph"""
        return sum(len(neighbors) for neighbors in self.adj.values())

    def has_node(self, node_id):
        """Check if a node exists in the graph"""
        return node_id in self.nodes

    def has_edge(self, from_node, to_node):
        """Check if an edge exists between two nodes"""
        return self.getEdgeWeight(from_node, to_node) is not None

    def get_node_coords(self, node_id):
        """
        Get the coordinates of a node.

        Args:
            node_id (int): Node ID

        Returns:
            tuple: (x, y) coordinates, or None if node doesn't exist
        """
        if node_id in self.nodes:
            name, coords = self.nodes[node_id]
            return coords
        return None

    def get_node_name(self, node_id):
        """
        Get the name of a node.

        Args:
            node_id (int): Node ID

        Returns:
            str: Node name, or None if node doesn't exist
        """
        if node_id in self.nodes:
            name, coords = self.nodes[node_id]
            return name
        return None