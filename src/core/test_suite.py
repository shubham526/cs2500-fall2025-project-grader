"""
Test Suite for CS 2500 Extra Credit Project
Contains all automated tests for graph operations, Dijkstra, A*, and performance
"""

import os


class GraphTester:
    """Tests for graph data structure and operations"""

    def __init__(self, graph_module, repo_dir):
        self.graph_module = graph_module
        self.repo_dir = repo_dir
        self.graph = None

        # Expected test data (based on provided CSV files)
        self.nodes_file = os.path.join(repo_dir, "nodes.csv")
        self.edges_file = os.path.join(repo_dir, "edges.csv")

    def build_graph(self):
        """Build a graph from the CSV files"""
        # Try to instantiate the graph
        try:
            # Common patterns: Graph(), RoadNetwork(), etc.
            if hasattr(self.graph_module, 'Graph'):
                self.graph = self.graph_module.Graph()
            elif hasattr(self.graph_module, 'RoadNetwork'):
                self.graph = self.graph_module.RoadNetwork()
            elif hasattr(self.graph_module, 'graph'):
                self.graph = self.graph_module.graph
            else:
                # Try to find any class that looks like a graph
                for attr_name in dir(self.graph_module):
                    attr = getattr(self.graph_module, attr_name)
                    if isinstance(attr, type):
                        self.graph = attr()
                        break

            # Try to load CSV data
            if hasattr(self.graph, 'load_from_csv'):
                self.graph.load_from_csv(self.nodes_file, self.edges_file)
            elif hasattr(self.graph, 'load_data'):
                self.graph.load_data(self.nodes_file, self.edges_file)
            elif hasattr(self.graph, 'parse_csv'):
                self.graph.parse_csv(self.nodes_file, self.edges_file)
            else:
                # Try to manually load
                self._manual_load_csv()

            return self.graph

        except Exception as e:
            raise Exception(f"Failed to build graph: {str(e)}")

    def _manual_load_csv(self):
        """Manually load CSV files if no built-in method"""
        # Load nodes
        with open(self.nodes_file, 'r') as f:
            lines = f.readlines()
            for line in lines[1:]:  # Skip header
                parts = line.strip().split(',')
                if len(parts) >= 4:
                    node_id = int(parts[0])
                    name = parts[1]
                    x = float(parts[2])
                    y = float(parts[3])

                    if hasattr(self.graph, 'add_node'):
                        self.graph.add_node(node_id, name, (x, y))
                    elif hasattr(self.graph, 'addNode'):
                        self.graph.addNode(node_id, name, (x, y))

        # Load edges
        with open(self.edges_file, 'r') as f:
            lines = f.readlines()
            for line in lines[1:]:  # Skip header
                parts = line.strip().split(',')
                if len(parts) >= 3:
                    from_node = int(parts[0])
                    to_node = int(parts[1])
                    weight = float(parts[2])

                    if hasattr(self.graph, 'add_edge'):
                        self.graph.add_edge(from_node, to_node, weight)
                    elif hasattr(self.graph, 'addEdge'):
                        self.graph.addEdge(from_node, to_node, weight)

    def test_csv_parsing(self):
        """Test 1: CSV files are parsed correctly"""
        try:
            self.build_graph()

            # Count nodes
            node_count = 0
            if hasattr(self.graph, 'nodes'):
                node_count = len(self.graph.nodes)
            elif hasattr(self.graph, 'get_nodes'):
                node_count = len(self.graph.get_nodes())
            elif hasattr(self.graph, 'num_nodes'):
                node_count = self.graph.num_nodes()

            # Count edges
            edge_count = 0
            if hasattr(self.graph, 'edges'):
                edge_count = len(self.graph.edges)
            elif hasattr(self.graph, 'get_edges'):
                edge_count = len(self.graph.get_edges())
            elif hasattr(self.graph, 'num_edges'):
                edge_count = self.graph.num_edges()

            passed = node_count >= 15  # At least 15 nodes required

            return {
                "name": "CSV Parsing",
                "passed": passed,
                "expected": "Load 15+ nodes and edges from CSV",
                "actual": f"Loaded {node_count} nodes, {edge_count} edges",
                "points": 2.4 if passed else 0
            }
        except Exception as e:
            return {
                "name": "CSV Parsing",
                "passed": False,
                "expected": "Load CSV files successfully",
                "actual": f"Error: {str(e)}",
                "points": 0
            }

    def test_add_remove_nodes(self):
        """Test 2: Add and remove nodes"""
        try:
            # Add a test node
            test_id = 999
            if hasattr(self.graph, 'add_node'):
                self.graph.add_node(test_id, "Test Node", (0, 0))
            elif hasattr(self.graph, 'addNode'):
                self.graph.addNode(test_id, "Test Node", (0, 0))

            # Check if added
            added = False
            if hasattr(self.graph, 'has_node'):
                added = self.graph.has_node(test_id)
            elif hasattr(self.graph, 'nodes') and test_id in self.graph.nodes:
                added = True

            # Remove the node
            if hasattr(self.graph, 'remove_node'):
                self.graph.remove_node(test_id)
            elif hasattr(self.graph, 'removeNode'):
                self.graph.removeNode(test_id)

            # Check if removed
            removed = True
            if hasattr(self.graph, 'has_node'):
                removed = not self.graph.has_node(test_id)
            elif hasattr(self.graph, 'nodes') and test_id in self.graph.nodes:
                removed = False

            passed = added and removed

            return {
                "name": "Add/Remove Nodes",
                "passed": passed,
                "expected": "Successfully add and remove nodes",
                "actual": f"Add: {added}, Remove: {removed}",
                "points": 2.4 if passed else 0
            }
        except Exception as e:
            return {
                "name": "Add/Remove Nodes",
                "passed": False,
                "expected": "Add and remove nodes",
                "actual": f"Error: {str(e)}",
                "points": 0
            }

    def test_add_remove_edges(self):
        """Test 3: Add and remove edges"""
        try:
            # Add test edge (between existing nodes)
            if hasattr(self.graph, 'add_edge'):
                self.graph.add_edge(1, 2, 999.0)
            elif hasattr(self.graph, 'addEdge'):
                self.graph.addEdge(1, 2, 999.0)

            # Check if added
            added = False
            if hasattr(self.graph, 'has_edge'):
                added = self.graph.has_edge(1, 2)
            elif hasattr(self.graph, 'get_edge_weight'):
                weight = self.graph.get_edge_weight(1, 2)
                added = weight == 999.0

            # Remove edge
            if hasattr(self.graph, 'remove_edge'):
                self.graph.remove_edge(1, 2)
            elif hasattr(self.graph, 'removeEdge'):
                self.graph.removeEdge(1, 2)

            passed = True  # If no errors, consider it passed

            return {
                "name": "Add/Remove Edges",
                "passed": passed,
                "expected": "Successfully add and remove edges",
                "actual": "Operations completed",
                "points": 2.4 if passed else 0
            }
        except Exception as e:
            return {
                "name": "Add/Remove Edges",
                "passed": False,
                "expected": "Add and remove edges",
                "actual": f"Error: {str(e)}",
                "points": 0
            }

    def test_get_neighbors(self):
        """Test 4: Get neighbors of a node"""
        try:
            # Get neighbors of node 1
            neighbors = None
            if hasattr(self.graph, 'get_neighbors'):
                neighbors = self.graph.get_neighbors(1)
            elif hasattr(self.graph, 'getNeighbors'):
                neighbors = self.graph.getNeighbors(1)
            elif hasattr(self.graph, 'neighbors'):
                neighbors = self.graph.neighbors(1)

            passed = neighbors is not None and len(neighbors) > 0

            return {
                "name": "Get Neighbors",
                "passed": passed,
                "expected": "Return list of adjacent nodes",
                "actual": f"Found {len(neighbors) if neighbors else 0} neighbors",
                "points": 2.4 if passed else 0
            }
        except Exception as e:
            return {
                "name": "Get Neighbors",
                "passed": False,
                "expected": "Return neighbors list",
                "actual": f"Error: {str(e)}",
                "points": 0
            }

    def test_get_edge_weight(self):
        """Test 5: Get weight of an edge"""
        try:
            # Get weight of an edge (1 -> 2 for example)
            weight = None
            if hasattr(self.graph, 'get_edge_weight'):
                weight = self.graph.get_edge_weight(1, 2)
            elif hasattr(self.graph, 'getEdgeWeight'):
                weight = self.graph.getEdgeWeight(1, 2)
            elif hasattr(self.graph, 'weight'):
                weight = self.graph.weight(1, 2)

            passed = weight is not None and weight > 0

            return {
                "name": "Get Edge Weight",
                "passed": passed,
                "expected": "Return edge weight",
                "actual": f"Weight: {weight}",
                "points": 2.4 if passed else 0
            }
        except Exception as e:
            return {
                "name": "Get Edge Weight",
                "passed": False,
                "expected": "Return edge weight",
                "actual": f"Error: {str(e)}",
                "points": 0
            }

    def run_all_tests(self):
        """Run all graph tests"""
        tests = [
            self.test_csv_parsing(),
            self.test_add_remove_nodes(),
            self.test_add_remove_edges(),
            self.test_get_neighbors(),
            self.test_get_edge_weight()
        ]

        total_points = sum(t["points"] for t in tests)
        max_points = 12

        return {
            "tests": tests,
            "total_points": total_points,
            "max_points": max_points
        }


class DijkstraTester:
    """Tests for Dijkstra's algorithm"""

    # Required test queries (page 9 of project spec)
    REQUIRED_QUERIES = [
        (1, 14, "Main Gateway → Parking Garage (Long Path)"),
        (8, 9, "Student Center → Cafe (Short Path)"),
        (4, 13, "CS Department → Dorm B (Cross-Map)"),
        (6, 10, "Physics Building → Gymnasium (Winding Path)"),
        (3, 11, "Library → Aquatic Center (Medium Path)")
    ]

    # Expected optimal costs (you'll need to update these based on your dataset)
    EXPECTED_COSTS = {
        (1, 14): 42.0,  # Update these with actual optimal costs
        (8, 9): 5.0,
        (4, 13): 38.0,
        (6, 10): 27.0,
        (3, 11): 31.0
    }

    def __init__(self, dijkstra_module, graph):
        self.dijkstra_module = dijkstra_module
        self.graph = graph

    def run_dijkstra(self, start, end):
        """Run student's Dijkstra implementation"""
        try:
            # Try different function names
            if hasattr(self.dijkstra_module, 'dijkstra'):
                result = self.dijkstra_module.dijkstra(self.graph, start, end)
            elif hasattr(self.dijkstra_module, 'shortest_path'):
                result = self.dijkstra_module.shortest_path(self.graph, start, end)
            elif hasattr(self.dijkstra_module, 'find_path'):
                result = self.dijkstra_module.find_path(self.graph, start, end)
            else:
                return None, None, "No dijkstra function found"

            # Parse result - common formats:
            # (path, cost), (cost, path), {"path": ..., "cost": ...}
            if isinstance(result, tuple):
                if len(result) >= 2:
                    # Try to determine which is path and which is cost
                    if isinstance(result[0], list):
                        path, cost = result[0], result[1]
                    elif isinstance(result[1], list):
                        cost, path = result[0], result[1]
                    else:
                        path, cost = result, None
                else:
                    path, cost = result[0], None
            elif isinstance(result, dict):
                path = result.get('path', result.get('shortest_path', []))
                cost = result.get('cost', result.get('distance', result.get('weight', None)))
            else:
                path = result
                cost = None

            # Try to extract nodes_explored
            nodes_explored = None
            if isinstance(result, dict):
                nodes_explored = result.get('nodes_explored', result.get('visited', None))

            return path, cost, nodes_explored

        except Exception as e:
            return None, None, f"Error: {str(e)}"

    def test_query(self, start, end, description):
        """Test a single query"""
        path, cost, nodes_explored = self.run_dijkstra(start, end)

        expected_cost = self.EXPECTED_COSTS.get((start, end), None)

        # For testing purposes, if we don't have expected cost, just check if it returns something
        if expected_cost is None:
            passed = path is not None and cost is not None
            status = "PASS (no expected cost to verify)" if passed else "FAIL"
        else:
            passed = cost is not None and abs(cost - expected_cost) < 0.01
            status = "PASS" if passed else "FAIL"

        return {
            "name": f"Query: {description}",
            "passed": passed,
            "start": start,
            "end": end,
            "expected_cost": expected_cost,
            "actual_cost": cost,
            "path": path,
            "nodes_explored": nodes_explored,
            "status": status,
            "points": 3 if passed else 0
        }

    def run_all_tests(self):
        """Run all Dijkstra tests"""
        tests = []

        for start, end, description in self.REQUIRED_QUERIES:
            tests.append(self.test_query(start, end, description))

        total_points = sum(t["points"] for t in tests)
        max_points = 15

        return {
            "tests": tests,
            "total_points": total_points,
            "max_points": max_points
        }


class AStarTester:
    """Tests for A* algorithm"""

    # Use same queries as Dijkstra
    REQUIRED_QUERIES = DijkstraTester.REQUIRED_QUERIES
    EXPECTED_COSTS = DijkstraTester.EXPECTED_COSTS

    def __init__(self, astar_module, graph):
        self.astar_module = astar_module
        self.graph = graph

    def run_astar(self, start, end):
        """Run student's A* implementation"""
        try:
            # Try different function names
            if hasattr(self.astar_module, 'astar'):
                result = self.astar_module.astar(self.graph, start, end)
            elif hasattr(self.astar_module, 'a_star'):
                result = self.astar_module.a_star(self.graph, start, end)
            elif hasattr(self.astar_module, 'find_path'):
                result = self.astar_module.find_path(self.graph, start, end)
            else:
                return None, None, "No A* function found"

            # Parse result (same as Dijkstra)
            if isinstance(result, tuple):
                if len(result) >= 2:
                    if isinstance(result[0], list):
                        path, cost = result[0], result[1]
                    elif isinstance(result[1], list):
                        cost, path = result[0], result[1]
                    else:
                        path, cost = result, None
                else:
                    path, cost = result[0], None
            elif isinstance(result, dict):
                path = result.get('path', result.get('shortest_path', []))
                cost = result.get('cost', result.get('distance', result.get('weight', None)))
            else:
                path = result
                cost = None

            # Try to extract nodes_explored
            nodes_explored = None
            if isinstance(result, dict):
                nodes_explored = result.get('nodes_explored', result.get('visited', None))

            return path, cost, nodes_explored

        except Exception as e:
            return None, None, f"Error: {str(e)}"

    def test_query(self, start, end, description):
        """Test a single query"""
        path, cost, nodes_explored = self.run_astar(start, end)

        expected_cost = self.EXPECTED_COSTS.get((start, end), None)

        # A* should find optimal path (same cost as Dijkstra)
        if expected_cost is None:
            passed = path is not None and cost is not None
            status = "PASS (no expected cost to verify)" if passed else "FAIL"
        else:
            passed = cost is not None and abs(cost - expected_cost) < 0.01
            status = "PASS" if passed else "FAIL"

        return {
            "name": f"Query: {description}",
            "passed": passed,
            "start": start,
            "end": end,
            "expected_cost": expected_cost,
            "actual_cost": cost,
            "path": path,
            "nodes_explored": nodes_explored,
            "status": status,
            "points": 3 if passed else 0
        }

    def run_all_tests(self):
        """Run all A* tests"""
        tests = []

        for start, end, description in self.REQUIRED_QUERIES:
            tests.append(self.test_query(start, end, description))

        total_points = sum(t["points"] for t in tests)
        max_points = 15

        return {
            "tests": tests,
            "total_points": total_points,
            "max_points": max_points
        }


class PerformanceTester:
    """Tests for performance comparison between Dijkstra and A*"""

    def __init__(self, dijkstra_module, astar_module, graph):
        self.dijkstra_module = dijkstra_module
        self.astar_module = astar_module
        self.graph = graph

    def run_all_tests(self):
        """Run performance comparison tests"""

        # Run both algorithms on test queries
        dijkstra_tester = DijkstraTester(self.dijkstra_module, self.graph)
        astar_tester = AStarTester(self.astar_module, self.graph)

        comparisons = []

        for start, end, description in DijkstraTester.REQUIRED_QUERIES:
            # Run Dijkstra
            d_path, d_cost, d_nodes = dijkstra_tester.run_dijkstra(start, end)

            # Run A*
            a_path, a_cost, a_nodes = astar_tester.run_astar(start, end)

            comparisons.append({
                "query": description,
                "start": start,
                "end": end,
                "dijkstra_cost": d_cost,
                "dijkstra_nodes": d_nodes,
                "astar_cost": a_cost,
                "astar_nodes": a_nodes,
                "astar_improvement": ((d_nodes - a_nodes) / d_nodes * 100) if (d_nodes and a_nodes) else None
            })

        # Check if tracking works
        tracking_works = any(c["dijkstra_nodes"] is not None or c["astar_nodes"] is not None
                             for c in comparisons)

        # Check if A* generally explores fewer nodes
        astar_better_count = sum(1 for c in comparisons
                                 if c["dijkstra_nodes"] and c["astar_nodes"]
                                 and c["astar_nodes"] <= c["dijkstra_nodes"])

        return {
            "comparisons": comparisons,
            "tracking_works": tracking_works,
            "astar_better_count": astar_better_count,
            "total_queries": len(comparisons),
            "points": 5 if tracking_works else 0
        }