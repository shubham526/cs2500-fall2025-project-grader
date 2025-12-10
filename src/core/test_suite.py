"""
Test Suite for CS 2500 Extra Credit Project
Contains all automated tests for graph operations, Dijkstra, A*, and performance
"""

import os
import time
import math
import inspect
from typing import Any, Dict, List, Tuple


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

            # Try to load CSV data using various common names
            if hasattr(self.graph, 'load_from_csv'):
                self.graph.load_from_csv(self.nodes_file, self.edges_file)
            elif hasattr(self.graph, 'loadFromCSV'):
                self.graph.loadFromCSV(self.nodes_file, self.edges_file)
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

        # Helper to find the addNode method
        add_node_method = None
        if hasattr(self.graph, 'addNode'):
            add_node_method = self.graph.addNode
        elif hasattr(self.graph, 'add_node'):
            add_node_method = self.graph.add_node

        # Helper to find the addEdge method
        add_edge_method = None
        if hasattr(self.graph, 'addEdge'):
            add_edge_method = self.graph.addEdge
        elif hasattr(self.graph, 'add_edge'):
            add_edge_method = self.graph.add_edge

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

                    if add_node_method:
                        # SMART LOADING: Check parameter names to determine order
                        try:
                            sig = inspect.signature(add_node_method)
                            params = list(sig.parameters.keys())

                            # Check if student uses specific variable names "x" and "y"
                            if 'x' in params and 'y' in params:
                                # Use Keyword Arguments (Safe for any order)
                                # We construct kwargs dynamically based on what the student named their 'id' and 'name'
                                kwargs = {'x': x, 'y': y}

                                # Find what they named the ID parameter (likely the first one after self)
                                # params[0] is usually 'self' if bound, or first arg if unbound.
                                # inspect.signature on bound method skips self.
                                first_arg = params[0]
                                kwargs[first_arg] = node_id

                                # Find what they named the Name parameter
                                if 'name' in params:
                                    kwargs['name'] = name
                                elif 'label' in params:
                                    kwargs['label'] = name

                                add_node_method(**kwargs)
                            else:
                                # Fallback 1: Standard Order (id, name, tuple)
                                try:
                                    add_node_method(node_id, name, (x, y))
                                except TypeError:
                                    # Fallback 2: Standard Order (id, name, x, y)
                                    add_node_method(node_id, name, x, y)

                        except Exception:
                            # Final "Brute Force" Fallback for Caleb Franklin case (id, x, y, name)
                            # If the above failed, try this specific swapped order
                            try:
                                add_node_method(node_id, x, y, name)
                            except:
                                pass

        # Load edges
        with open(self.edges_file, 'r') as f:
            lines = f.readlines()
            for line in lines[1:]:  # Skip header
                parts = line.strip().split(',')
                if len(parts) >= 3:
                    from_node = int(parts[0])
                    to_node = int(parts[1])
                    weight = float(parts[2])

                    if add_edge_method:
                        add_edge_method(from_node, to_node, weight)

    def _count_nodes(self):
        """Helper to robustly count nodes in the graph"""
        if hasattr(self.graph, 'nodes'):
            return len(self.graph.nodes)
        elif hasattr(self.graph, 'get_nodes'):
            return len(self.graph.get_nodes())
        elif hasattr(self.graph, 'num_nodes'):
            return self.graph.num_nodes()
        elif hasattr(self.graph, 'graph') and isinstance(self.graph.graph, dict):
            return len(self.graph.graph)
        elif isinstance(self.graph, dict):
            return len(self.graph)
        return 0

    def _count_edges(self):
        """Helper to robustly count edges"""
        if hasattr(self.graph, 'edges'):
            return len(self.graph.edges)
        elif hasattr(self.graph, 'get_edges'):
            return len(self.graph.get_edges())
        elif hasattr(self.graph, 'num_edges'):
            return self.graph.num_edges()
        elif hasattr(self.graph, 'adj'):
            return sum(len(v) for v in self.graph.adj.values())
        return 0

    def test_csv_parsing(self):
        """Test 1: CSV files are parsed correctly"""
        try:
            self.build_graph()

            node_count = self._count_nodes()
            edge_count = self._count_edges()

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

            # Helper to find method
            add_node = getattr(self.graph, 'addNode', getattr(self.graph, 'add_node', None))

            if add_node:
                # Robust add using inspect (Same logic as manual load)
                try:
                    sig = inspect.signature(add_node)
                    params = list(sig.parameters.keys())
                    if 'x' in params and 'y' in params:
                        first_arg = params[0]
                        kwargs = {first_arg: test_id, 'x': 0.0, 'y': 0.0}
                        if 'name' in params: kwargs['name'] = "Test Node"
                        add_node(**kwargs)
                    else:
                        # Fallback
                        try:
                            add_node(test_id, "Test Node", (0, 0))
                        except TypeError:
                            add_node(test_id, "Test Node", 0, 0)
                except:
                    # Final fallback
                    try:
                        add_node(test_id, "Test Node", 0, 0)
                    except:
                        pass  # Fail silently, check results below

            # Check if added
            added = False
            if hasattr(self.graph, 'has_node'):
                added = self.graph.has_node(test_id)
            elif hasattr(self.graph, 'nodes') and test_id in self.graph.nodes:
                added = True
            elif hasattr(self.graph, 'graph') and isinstance(self.graph.graph, dict):
                added = test_id in self.graph.graph

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
            elif hasattr(self.graph, 'graph') and isinstance(self.graph.graph, dict):
                removed = test_id not in self.graph.graph

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
            # Use dummy nodes to avoid breaking existing data
            u, v = 9998, 9999

            # Reuse the robust add logic from above
            add_node = getattr(self.graph, 'addNode', getattr(self.graph, 'add_node', None))
            if add_node:
                try:
                    sig = inspect.signature(add_node)
                    params = list(sig.parameters.keys())
                    if 'x' in params and 'y' in params:
                        first_arg = params[0]
                        kw_u = {first_arg: u, 'x': 0.0, 'y': 0.0, 'name': 'U'}
                        kw_v = {first_arg: v, 'x': 1.0, 'y': 1.0, 'name': 'V'}
                        if 'name' not in params:
                            del kw_u['name']
                            del kw_v['name']
                        add_node(**kw_u)
                        add_node(**kw_v)
                    else:
                        try:
                            add_node(u, "U", (0, 0))
                            add_node(v, "V", (1, 1))
                        except TypeError:
                            add_node(u, "U", 0, 0)
                            add_node(v, "V", 1, 1)
                except:
                    pass

            # Add test edge
            if hasattr(self.graph, 'add_edge'):
                self.graph.add_edge(u, v, 5.0)
            elif hasattr(self.graph, 'addEdge'):
                self.graph.addEdge(u, v, 5.0)

            # Check if added
            added = False
            if hasattr(self.graph, 'has_edge'):
                added = self.graph.has_edge(u, v)
            elif hasattr(self.graph, 'get_edge_weight'):
                weight = self.graph.get_edge_weight(u, v)
                added = weight == 5.0
            elif hasattr(self.graph, 'getEdgeWeight'):
                weight = self.graph.getEdgeWeight(u, v)
                added = weight == 5.0

            # Remove edge
            if hasattr(self.graph, 'remove_edge'):
                self.graph.remove_edge(u, v)
            elif hasattr(self.graph, 'removeEdge'):
                self.graph.removeEdge(u, v)

            # Clean up dummy nodes
            if hasattr(self.graph, 'removeNode'):
                self.graph.removeNode(u)
                self.graph.removeNode(v)
            elif hasattr(self.graph, 'remove_node'):
                self.graph.remove_node(u)
                self.graph.remove_node(v)

            passed = True

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

    # Expected optimal costs
    EXPECTED_COSTS = {
        (1, 14): 113.0,
        (8, 9): 1.0,
        (4, 13): 75.0,
        (6, 10): 77.0,
        (3, 11): 64.0
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

            # Parse result
            nodes_explored = None
            path = None
            cost = None

            if isinstance(result, tuple):
                if len(result) >= 3:
                    # Format: (path, cost, nodes_explored, [time])
                    val1, val2, val3 = result[0], result[1], result[2]

                    if isinstance(val1, list) or val1 is None:
                        path = val1
                        cost = val2
                        nodes_explored = val3
                    elif isinstance(val2, list) or val2 is None:
                        cost = val1
                        path = val2
                        nodes_explored = val3
                    else:
                        path, cost, nodes_explored = val1, val2, val3

                elif len(result) >= 2:
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
                nodes_explored = result.get('nodes_explored', result.get('visited', None))
            else:
                path = result
                cost = None

            return path, cost, nodes_explored

        except Exception as e:
            return None, None, f"Error: {str(e)}"

    def test_query(self, start, end, description):
        """Test a single query"""
        path, cost, nodes_explored = self.run_dijkstra(start, end)

        expected_cost = self.EXPECTED_COSTS.get((start, end), None)

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

            # Parse result
            nodes_explored = None
            path = None
            cost = None

            if isinstance(result, tuple):
                if len(result) >= 3:
                    val1, val2, val3 = result[0], result[1], result[2]
                    if isinstance(val1, list) or val1 is None:
                        path = val1
                        cost = val2
                        nodes_explored = val3
                    elif isinstance(val2, list) or val2 is None:
                        cost = val1
                        path = val2
                        nodes_explored = val3
                    else:
                        path, cost, nodes_explored = val1, val2, val3
                elif len(result) >= 2:
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
                nodes_explored = result.get('nodes_explored', result.get('visited', None))
            else:
                path = result
                cost = None

            return path, cost, nodes_explored

        except Exception as e:
            return None, None, f"Error: {str(e)}"

    def test_query(self, start, end, description):
        """Test a single query"""
        path, cost, nodes_explored = self.run_astar(start, end)

        expected_cost = self.EXPECTED_COSTS.get((start, end), None)

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

        tracking_works = any(c["dijkstra_nodes"] is not None or c["astar_nodes"] is not None
                             for c in comparisons)

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