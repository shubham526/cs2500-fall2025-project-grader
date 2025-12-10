#!/usr/bin/env python3
"""
Test script to verify if student's graph code is correct
Tests the exact same operations the autograder uses
"""

# Student's code (copy-pasted)
import csv


class Graph:
    def __init__(self):
        # adjacency list: node_id -> list of (neighbor, weight)
        self.adj = {}
        # store node metadata: id -> (name, (x, y))
        self.nodes = {}

    def addNode(self, node_id, name, coords):
        self.nodes[node_id] = (name, coords)
        if node_id not in self.adj:
            self.adj[node_id] = []

    def addEdge(self, u, v, weight):
        if u not in self.adj:
            self.adj[u] = []
        self.adj[u].append((v, weight))

    def removeNode(self, node_id):
        if node_id in self.adj:
            del self.adj[node_id]
        if node_id in self.nodes:
            del self.nodes[node_id]
        # remove incoming edges to this node
        for src in self.adj:
            self.adj[src] = [(v, w) for (v, w) in self.adj[src] if v != node_id]

    def removeEdge(self, u, v):
        if u in self.adj:
            self.adj[u] = [(nbr, w) for (nbr, w) in self.adj[u] if nbr != v]

    def getNeighbors(self, node_id):
        return self.adj.get(node_id, [])

    def getEdgeWeight(self, u, v):
        for (nbr, w) in self.adj.get(u, []):
            if nbr == v:
                return w
        return None

    def load_from_csv(self, nodes_path, edges_path):
        # load nodes.csv
        with open(nodes_path, newline='') as f:
            reader = csv.reader(f)
            next(reader, None)  # skip header
            for row in reader:
                if not row:
                    continue
                node_id = int(row[0])
                name = row[1]
                x = float(row[2])
                y = float(row[3])
                self.addNode(node_id, name, (x, y))
        # load edges.csv
        with open(edges_path, newline='') as f:
            reader = csv.reader(f)
            next(reader, None)  # skip header
            for row in reader:
                if not row:
                    continue
                u = int(row[0])
                v = int(row[1])
                w = float(row[2])
                self.addEdge(u, v, w)


def test_student_code():
    """Test the student's Graph class directly"""

    print("=" * 60)
    print("TESTING STUDENT'S GRAPH CODE")
    print("=" * 60)

    # Test 1: Basic operations (no CSV)
    print("\n[Test 1] Basic Graph Operations (no CSV)")
    print("-" * 60)
    g = Graph()

    # Add nodes
    g.addNode(1, "Node1", (0.0, 0.0))
    g.addNode(2, "Node2", (1.0, 1.0))
    g.addNode(3, "Node3", (2.0, 2.0))
    print(f"✓ Added 3 nodes")
    print(f"  Nodes dict: {len(g.nodes)} entries")
    print(f"  Adj dict: {len(g.adj)} entries")

    # Add edges
    g.addEdge(1, 2, 5.5)
    g.addEdge(1, 3, 7.2)
    g.addEdge(2, 3, 3.1)
    print(f"✓ Added 3 edges")

    # Test getNeighbors
    neighbors = g.getNeighbors(1)
    print(f"\n  getNeighbors(1): {neighbors}")
    print(f"  Expected: [(2, 5.5), (3, 7.2)]")
    print(f"  Match: {neighbors == [(2, 5.5), (3, 7.2)]}")

    # Test getEdgeWeight (THIS IS THE FAILING TEST)
    weight_1_2 = g.getEdgeWeight(1, 2)
    print(f"\n  getEdgeWeight(1, 2): {weight_1_2}")
    print(f"  Expected: 5.5")
    print(f"  Match: {weight_1_2 == 5.5}")
    print(f"  Is None: {weight_1_2 is None}")
    print(f"  Is > 0: {weight_1_2 is not None and weight_1_2 > 0}")

    if weight_1_2 is None:
        print(f"\n❌ ERROR: getEdgeWeight returned None!")
        print(f"  adj[1] = {g.adj.get(1)}")
        return False
    else:
        print(f"\n✓ SUCCESS: getEdgeWeight works correctly")

    # Test 2: CSV Loading (if files available)
    print("\n[Test 2] CSV Loading")
    print("-" * 60)

    import os
    if os.path.exists("nodes.csv") and os.path.exists("edges.csv"):
        g2 = Graph()
        g2.load_from_csv("nodes.csv", "edges.csv")

        print(f"✓ Loaded from CSV")
        print(f"  Nodes: {len(g2.nodes)}")

        # Count edges
        edge_count = sum(len(neighbors) for neighbors in g2.adj.values())
        print(f"  Edges: {edge_count}")

        # Check if node 1 exists
        if 1 in g2.nodes:
            print(f"\n  Node 1 exists: {g2.nodes[1]}")
            print(f"  Node 1 neighbors: {g2.getNeighbors(1)}")

            # Check if edge 1->2 exists
            weight = g2.getEdgeWeight(1, 2)
            print(f"  Edge 1->2 weight: {weight}")

            if weight is None:
                print(f"\n⚠️  Edge 1->2 doesn't exist in CSV data")
                print(f"     This might be expected if your dataset doesn't have this edge")

                # Show what edges DO exist from node 1
                if 1 in g2.adj and g2.adj[1]:
                    first_edge = g2.adj[1][0]
                    print(f"     Testing with first available edge from node 1: 1->{first_edge[0]}")
                    test_weight = g2.getEdgeWeight(1, first_edge[0])
                    print(f"     Weight: {test_weight}")
                    print(f"     Test passes: {test_weight is not None and test_weight > 0}")
        else:
            print(f"  Node 1 doesn't exist in CSV")
    else:
        print(f"  Skipping CSV test (files not found)")
        print(f"  Looking for: nodes.csv, edges.csv")
        print(f"  Current directory: {os.getcwd()}")

    return True


if __name__ == "__main__":
    try:
        test_student_code()
    except Exception as e:
        print(f"\n❌ EXCEPTION: {e}")
        import traceback

        traceback.print_exc()