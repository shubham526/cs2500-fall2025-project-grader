#!/usr/bin/env python3
"""
Comprehensive diagnostic to find why getEdgeWeight test fails
Run this in the student's repo directory with your dataset
"""

import sys
import os

print("=" * 70)
print("COMPREHENSIVE DIAGNOSTIC FOR GRAPH getEdgeWeight FAILURE")
print("=" * 70)

# Step 1: Check files exist
print("\n[Step 1] Checking files...")
print("-" * 70)
files_to_check = ["graph.py", "nodes.csv", "edges.csv"]
for fname in files_to_check:
    exists = os.path.exists(fname)
    print(f"  {fname}: {'✓ EXISTS' if exists else '❌ MISSING'}")
    if exists and fname.endswith('.csv'):
        with open(fname, 'r') as f:
            lines = f.readlines()
            print(f"    Lines: {len(lines)} (including header)")
            if lines:
                print(f"    Header: {lines[0].strip()}")

if not all(os.path.exists(f) for f in files_to_check):
    print("\n❌ Missing required files. Cannot continue.")
    sys.exit(1)

# Step 2: Load and test student's graph
print("\n[Step 2] Testing student's Graph class...")
print("-" * 70)

try:
    from graph import Graph

    print("✓ Imported Graph class")
except Exception as e:
    print(f"❌ Failed to import Graph: {e}")
    sys.exit(1)

# Create instance
try:
    g = Graph()
    print("✓ Created Graph instance")
except Exception as e:
    print(f"❌ Failed to create Graph: {e}")
    sys.exit(1)

# Check if load_from_csv exists
if hasattr(g, 'load_from_csv'):
    print("✓ Has load_from_csv method")
else:
    print("❌ No load_from_csv method")
    sys.exit(1)

# Load CSV data
print("\n[Step 3] Loading CSV data...")
print("-" * 70)
try:
    g.load_from_csv("nodes.csv", "edges.csv")
    print("✓ load_from_csv() executed without error")
except Exception as e:
    print(f"❌ load_from_csv() failed: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)

# Check what was loaded
print("\n[Step 4] Checking loaded data...")
print("-" * 70)

# Count nodes
if hasattr(g, 'nodes'):
    print(f"✓ Graph has 'nodes' attribute")
    print(f"  Nodes loaded: {len(g.nodes)}")
    print(f"  Node IDs: {sorted(g.nodes.keys())}")
else:
    print(f"❌ Graph has no 'nodes' attribute")

# Count edges via adjacency list
if hasattr(g, 'adj'):
    print(f"\n✓ Graph has 'adj' attribute")
    total_edges = sum(len(neighbors) for neighbors in g.adj.values())
    print(f"  Total edges: {total_edges}")

    # Show adjacency list summary
    print(f"\n  Adjacency list summary:")
    for node_id in sorted(g.adj.keys())[:10]:  # First 10 nodes
        neighbors = g.adj[node_id]
        if neighbors:
            print(f"    Node {node_id}: {len(neighbors)} edges → {neighbors[:3]}{'...' if len(neighbors) > 3 else ''}")
        else:
            print(f"    Node {node_id}: 0 edges")
else:
    print(f"❌ Graph has no 'adj' attribute")

# Step 5: Test getEdgeWeight specifically
print("\n[Step 5] Testing getEdgeWeight method...")
print("-" * 70)

if not hasattr(g, 'getEdgeWeight'):
    print(f"❌ Graph has no 'getEdgeWeight' method")
    sys.exit(1)

print(f"✓ Graph has getEdgeWeight method")

# Test with edge 1 -> 2 (what the autograder tests)
print(f"\n  Testing getEdgeWeight(1, 2):")
weight = g.getEdgeWeight(1, 2)
print(f"    Result: {weight}")
print(f"    Type: {type(weight)}")
print(f"    Is None: {weight is None}")
if weight is not None:
    print(f"    Value > 0: {weight > 0}")
    print(f"    ✓ TEST WOULD PASS")
else:
    print(f"    ❌ TEST WOULD FAIL (weight is None)")

# If edge 1->2 doesn't exist, explain why
if weight is None:
    print(f"\n  Why is edge 1->2 None?")

    # Check if node 1 exists
    if 1 not in g.nodes:
        print(f"    ❌ Node 1 doesn't exist in graph")
    else:
        print(f"    ✓ Node 1 exists: {g.nodes[1]}")

    # Check if node 1 has any edges
    if 1 not in g.adj or not g.adj[1]:
        print(f"    ❌ Node 1 has NO outgoing edges")
        print(f"       This means edges.csv has no rows with from=1")
    else:
        print(f"    ✓ Node 1 has {len(g.adj[1])} outgoing edges:")
        for neighbor, w in g.adj[1]:
            print(f"        1 → {neighbor} (weight: {w})")
        print(f"    ❌ But edge 1→2 specifically doesn't exist")

    # Check if node 2 exists
    if 2 not in g.nodes:
        print(f"    ❌ Node 2 doesn't exist in graph")
    else:
        print(f"    ✓ Node 2 exists: {g.nodes[2]}")

# Step 6: Check the actual CSV file
print(f"\n[Step 6] Examining edges.csv directly...")
print("-" * 70)

with open("edges.csv", 'r') as f:
    lines = f.readlines()
    print(f"Total lines in edges.csv: {len(lines)}")
    print(f"Header: {lines[0].strip()}")

    # Check if edge 1->2 exists in file
    print(f"\nSearching for edge 1→2 in file...")
    found_1_to_2 = False
    edges_from_1 = []

    for i, line in enumerate(lines[1:], 1):  # Skip header
        parts = line.strip().split(',')
        if len(parts) >= 3:
            from_node = parts[0].strip()
            to_node = parts[1].strip()

            if from_node == '1':
                edges_from_1.append((to_node, parts[2]))
                if to_node == '2':
                    found_1_to_2 = True
                    print(f"  ✓ FOUND at line {i + 1}: {line.strip()}")

    if not found_1_to_2:
        print(f"  ❌ Edge 1→2 NOT FOUND in edges.csv")
        if edges_from_1:
            print(f"  Edges from node 1 in file:")
            for to_node, weight in edges_from_1:
                print(f"    1 → {to_node} (weight: {weight})")
        else:
            print(f"  No edges from node 1 at all in file!")

# Step 7: Test with an edge that DOES exist
print(f"\n[Step 7] Testing with an edge that exists...")
print("-" * 70)

# Find ANY edge that exists
test_edge = None
if hasattr(g, 'adj'):
    for node_id in sorted(g.adj.keys()):
        if g.adj[node_id]:
            neighbor, weight = g.adj[node_id][0]
            test_edge = (node_id, neighbor, weight)
            break

if test_edge:
    from_node, to_node, expected_weight = test_edge
    print(f"Testing with edge {from_node}→{to_node} (expected weight: {expected_weight})")

    result = g.getEdgeWeight(from_node, to_node)
    print(f"  getEdgeWeight({from_node}, {to_node}) = {result}")
    print(f"  Expected: {expected_weight}")
    print(f"  Match: {result == expected_weight}")

    if result == expected_weight:
        print(f"\n  ✓ getEdgeWeight() WORKS CORRECTLY!")
        print(f"  ❌ But the autograder tests edge 1→2 which doesn't exist in your dataset")
    else:
        print(f"\n  ❌ getEdgeWeight() returns wrong value")
else:
    print(f"  ❌ No edges found in graph at all")

# Final diagnosis
print(f"\n{'=' * 70}")
print(f"DIAGNOSIS")
print(f"{'=' * 70}")

if weight is not None:
    print(f"✓ Student's code is CORRECT - getEdgeWeight works")
    print(f"✓ Test passes")
elif test_edge and g.getEdgeWeight(test_edge[0], test_edge[1]) == test_edge[2]:
    print(f"✓ Student's code is CORRECT - getEdgeWeight works")
    print(f"❌ BUT: Your dataset doesn't have edge 1→2")
    print(f"🔧 FIX: Either:")
    print(f"   1. Add edge 1→2 to your edges.csv, OR")
    print(f"   2. Change test to use an edge that exists in your dataset")
else:
    print(f"❌ Student's code has a BUG in getEdgeWeight")
    print(f"   (or the graph didn't load properly)")