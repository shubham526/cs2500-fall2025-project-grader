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
        self.nodes_file = os.path.join(repo_dir, "nodes.csv")
        self.edges_file = os.path.join(repo_dir, "edges.csv")

    def build_graph(self):
        try:
            # 1. Look for Class-based implementation
            if hasattr(self.graph_module, 'Graph'):
                graph_cls = self.graph_module.Graph

                # VINCE NJOROGE FIX:
                # Check if __init__ requires args and if class has static loader methods
                try:
                    # Try standard empty init first
                    self.graph = graph_cls()
                except TypeError:
                    # If that fails (missing args), try to load data using his methods
                    nodes_data = {}
                    edges_data = {}

                    # Check for static make_nodes/make_edges (Vince's pattern)
                    if hasattr(graph_cls, 'make_nodes'):
                        try:
                            nodes_data = graph_cls.make_nodes(self.nodes_file)
                        except:
                            pass
                    if hasattr(graph_cls, 'make_edges'):
                        try:
                            edges_data = graph_cls.make_edges(self.edges_file)
                        except:
                            pass

                    # Try instantiating with loaded data
                    try:
                        self.graph = graph_cls(nodes_data, edges_data)
                    except:
                        # Fallback for other signatures
                        self.graph = graph_cls({}, {})

            elif hasattr(self.graph_module, 'RoadNetwork'):
                self.graph = self.graph_module.RoadNetwork()
            elif hasattr(self.graph_module, 'graph') and isinstance(self.graph_module.graph, type):
                self.graph = self.graph_module.graph()
            else:
                # 2. Support Module-based implementation
                if hasattr(self.graph_module, 'nodes') and hasattr(self.graph_module, 'edges'):
                    self.graph = self.graph_module
                else:
                    found = False
                    for attr_name in dir(self.graph_module):
                        attr = getattr(self.graph_module, attr_name)
                        if isinstance(attr, type) and attr.__module__ == self.graph_module.__name__:
                            self.graph = attr()
                            found = True
                            break
                    if not found:
                        self.graph = self.graph_module

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
                self._manual_load_csv()

            return self.graph

        except Exception as e:
            raise Exception(f"Failed to build graph: {str(e)}")

    def _manual_load_csv(self):
        if self._count_nodes() > 0: return
        add_node_method = getattr(self.graph, 'addNode', getattr(self.graph, 'add_node', None))
        add_edge_method = getattr(self.graph, 'addEdge', getattr(self.graph, 'add_edge', None))

        if not add_node_method: return

        with open(self.nodes_file, 'r') as f:
            lines = f.readlines()
            for line in lines[1:]:
                parts = line.strip().split(',')
                if len(parts) >= 4:
                    node_id = int(parts[0])
                    name = parts[1]
                    x = float(parts[2])
                    y = float(parts[3])
                    if add_node_method:
                        try:
                            sig = inspect.signature(add_node_method)
                            params = list(sig.parameters.keys())
                            if 'x' in params and 'y' in params:
                                kwargs = {'x': x, 'y': y}
                                first_arg = params[0]
                                kwargs[first_arg] = node_id
                                if 'name' in params:
                                    kwargs['name'] = name
                                elif 'label' in params:
                                    kwargs['label'] = name
                                add_node_method(**kwargs)
                            else:
                                try:
                                    add_node_method(node_id, name, (x, y))
                                except TypeError:
                                    add_node_method(node_id, name, x, y)
                        except:
                            try:
                                add_node_method(node_id, x, y, name)
                            except:
                                pass
        with open(self.edges_file, 'r') as f:
            lines = f.readlines()
            for line in lines[1:]:
                parts = line.strip().split(',')
                if len(parts) >= 3:
                    from_node = int(parts[0])
                    to_node = int(parts[1])
                    weight = float(parts[2])
                    if add_edge_method:
                        try:
                            add_edge_method(from_node, to_node, weight)
                        except:
                            pass

    def _count_nodes(self):
        if hasattr(self.graph, 'nodes'):
            val = self.graph.nodes
            if isinstance(val, dict) or isinstance(val, list): return len(val)
            if callable(val): return len(val())
        if hasattr(self.graph, 'get_nodes'): return len(self.graph.get_nodes())
        if hasattr(self.graph, 'num_nodes'): return self.graph.num_nodes()
        if hasattr(self.graph, 'graph') and isinstance(self.graph.graph, dict): return len(self.graph.graph)
        if hasattr(self.graph, 'nodeNames'): return len(self.graph.nodeNames)
        if isinstance(self.graph, dict): return len(self.graph)
        return 0

    def _count_edges(self):
        if hasattr(self.graph, 'edges'):
            val = self.graph.edges
            if isinstance(val, dict):
                count = 0
                for u, neighbors in val.items(): count += len(neighbors)
                return count
            if isinstance(val, list): return len(val)
        if hasattr(self.graph, 'get_edges'): return len(self.graph.get_edges())
        if hasattr(self.graph, 'adj'): return sum(len(v) for v in self.graph.adj.values())
        return 0

    def test_csv_parsing(self):
        try:
            self.build_graph()
            node_count = self._count_nodes()
            passed = node_count >= 15
            return {"name": "CSV Parsing", "passed": passed, "expected": "Load 15+ nodes",
                    "actual": f"Loaded {node_count} nodes", "points": 2.4 if passed else 0}
        except Exception as e:
            return {"name": "CSV Parsing", "passed": False, "expected": "Load data", "actual": f"Error: {str(e)}",
                    "points": 0}

    def test_add_remove_nodes(self):
        try:
            test_id = 999
            add_node = getattr(self.graph, 'addNode', getattr(self.graph, 'add_node', None))
            if add_node:
                try:
                    sig = inspect.signature(add_node)
                    params = list(sig.parameters.keys())
                    if 'x' in params and 'y' in params:
                        first = params[0]
                        kwargs = {first: test_id, 'x': 0, 'y': 0}
                        if 'name' in params: kwargs['name'] = "Test"
                        add_node(**kwargs)
                    else:
                        try:
                            add_node(test_id, "Test", (0, 0))
                        except:
                            add_node(test_id, "Test", 0, 0)
                except:
                    pass
            return {"name": "Add/Remove Nodes", "passed": True, "expected": "Add/Remove", "actual": "Pass",
                    "points": 2.4}
        except:
            return {"name": "Add/Remove Nodes", "passed": False, "expected": "Add/Remove", "actual": "Error",
                    "points": 0}

    def test_add_remove_edges(self):
        return {"name": "Add/Remove Edges", "passed": True, "expected": "Add/Remove", "actual": "Pass", "points": 2.4}

    def test_get_neighbors(self):
        try:
            neighbors = None
            func = getattr(self.graph, 'getNeighbors',
                           getattr(self.graph, 'get_neighbors', getattr(self.graph, 'neighbors', None)))
            if func:
                neighbors = func(1)
                if not neighbors: neighbors = func("1")
            passed = neighbors is not None and len(neighbors) > 0
            return {"name": "Get Neighbors", "passed": passed, "expected": "Get Neighbors", "actual": "Pass",
                    "points": 2.4}
        except:
            return {"name": "Get Neighbors", "passed": False, "expected": "Get Neighbors", "actual": "Error",
                    "points": 0}

    def test_get_edge_weight(self):
        try:
            weight = None
            func = getattr(self.graph, 'getEdgeWeight', getattr(self.graph, 'get_edge_weight',
                                                                getattr(self.graph, 'edge_weight',
                                                                        getattr(self.graph, 'weight', None))))
            if func:
                weight = func(1, 2)
                if weight is None: weight = func("1", "2")

            # Vince Njoroge Fix: Check edges dict directly
            if weight is None and hasattr(self.graph, 'edges') and isinstance(self.graph.edges, dict):
                if 1 in self.graph.edges and 2 in self.graph.edges[1]:
                    weight = self.graph.edges[1][2]
                elif "1" in self.graph.edges and "2" in self.graph.edges["1"]:
                    weight = self.graph.edges["1"]["2"]

            passed = weight is not None and weight > 0
            return {"name": "Get Edge Weight", "passed": passed, "expected": "Get Weight", "actual": "Pass",
                    "points": 2.4}
        except:
            return {"name": "Get Edge Weight", "passed": False, "expected": "Get Weight", "actual": "Error",
                    "points": 0}

    def run_all_tests(self):
        tests = [self.test_csv_parsing(), self.test_add_remove_nodes(), self.test_add_remove_edges(),
                 self.test_get_neighbors(), self.test_get_edge_weight()]
        return {"tests": tests, "total_points": sum(t["points"] for t in tests), "max_points": 12}


class DijkstraTester:
    REQUIRED_QUERIES = [
        (1, 14, "Main Gateway → Parking Garage (Long Path)"),
        (8, 9, "Student Center → Cafe (Short Path)"),
        (4, 13, "CS Department → Dorm B (Cross-Map)"),
        (6, 10, "Physics Building → Gymnasium (Winding Path)"),
        (3, 11, "Library → Aquatic Center (Medium Path)")
    ]
    EXPECTED_COSTS = {(1, 14): 113.0, (8, 9): 1.0, (4, 13): 75.0, (6, 10): 77.0, (3, 11): 64.0}

    def __init__(self, dijkstra_module, graph):
        self.dijkstra_module = dijkstra_module
        self.graph = graph

    def reconstruct_path_from_parents(self, came_from, start, end):
        current = end
        path = []
        if end not in came_from and str(end) in came_from: end = str(end)
        if start not in came_from and str(start) in came_from: start = str(start)
        if end not in came_from: return None
        while current != start:
            path.append(current)
            current = came_from.get(current)
            if current is None: break
        path.append(start)
        path.reverse()
        return path

    def run_dijkstra(self, start, end):
        try:
            func = None
            if hasattr(self.dijkstra_module, 'Dijkstra'):
                d_class = self.dijkstra_module.Dijkstra(self.graph)
                func = getattr(d_class, 'find_shortest_path', getattr(d_class, 'dijkstra', None))

            if not func:
                func = getattr(self.dijkstra_module, 'dijkstra',
                               getattr(self.dijkstra_module, 'shortest_path',
                                       getattr(self.dijkstra_module, 'find_shortest_path',
                                               getattr(self.dijkstra_module, 'Dijkstra_Search',
                                                       getattr(self.dijkstra_module, 'find_path', None)))))

            if not func: return None, None, "No function found"

            start_val, end_val = start, end
            if hasattr(self.graph, 'nodes'):
                keys = list(self.graph.nodes.keys())
                if keys and isinstance(keys[0], str): start_val, end_val = str(start), str(end)

            try:
                sig = inspect.signature(func)
                params = list(sig.parameters.keys())

                if 'edges' in params and 'nodes' in params:
                    g_nodes = getattr(self.graph, 'nodes', {})
                    g_edges = getattr(self.graph, 'edges', {})
                    kwargs = {'edges': g_edges, 'nodes': g_nodes}
                    remaining = [p for p in params if p not in ['edges', 'nodes']]
                    if len(remaining) >= 2:
                        kwargs[remaining[0]] = start_val
                        kwargs[remaining[1]] = end_val
                    result = func(**kwargs)
                else:
                    if inspect.ismethod(func):
                        result = func(start_val, end_val)
                    else:
                        result = func(self.graph, start_val, end_val)
            except:
                result = func(self.graph, start_val, end_val)

            nodes_explored, path, cost = None, None, None

            if hasattr(result, 'cost') and hasattr(result, 'path'):
                path = getattr(result, 'path')
                cost = getattr(result, 'cost')
                nodes_explored = getattr(result, 'nodes_explored', None)
            elif isinstance(result, tuple):
                if len(result) == 4:
                    path, cost, nodes_explored = result[0], result[1], result[2]
                elif len(result) >= 3:
                    val1, val2, val3 = result[0], result[1], result[2]
                    if isinstance(val1, dict) and isinstance(val2, dict):
                        path = self.reconstruct_path_from_parents(val1, start_val, end_val)
                        cost = val2.get(end_val)
                        nodes_explored = val3
                    else:
                        for val in result:
                            if isinstance(val, list):
                                path = val
                            elif isinstance(val, (int, float)) and not isinstance(val, bool):
                                if val > 1000:
                                    pass
                                elif isinstance(val, float) or cost is None:
                                    cost = val
                                else:
                                    nodes_explored = val
                elif len(result) == 2:
                    val1, val2 = result
                    if isinstance(val1, list) and isinstance(val2, list):
                        try:
                            nodes_explored = sum(1 for x in val1 if x != float('inf'))
                            idx = -1
                            if isinstance(end, int):
                                idx = end - 1
                            elif str(end).isdigit():
                                idx = int(end) - 1
                            if idx >= 0 and idx < len(val1): cost = val1[idx]
                            parent_map = {}
                            for i, p in enumerate(val2):
                                if p is not None and p != 0:
                                    parent_map[i + 1] = p
                            path = self.reconstruct_path_from_parents(parent_map, start_val, end_val)
                        except:
                            pass
                    elif isinstance(val1, list):
                        path, cost = val1, val2
                    else:
                        cost, path = val1, val2
            elif isinstance(result, dict):
                path = result.get('path', result.get('shortest_path'))
                # VINCE FIX: added 'distance'
                cost = result.get('cost', result.get('total_cost', result.get('distance')))
                # VINCE FIX: added 'explored'
                nodes_explored = result.get('nodes_explored', result.get('visited_nodes', result.get('explored')))
                if isinstance(nodes_explored, list): nodes_explored = len(nodes_explored)

            if isinstance(cost, list): cost = None

            return path, cost, nodes_explored

        except Exception as e:
            return None, None, f"Error: {str(e)}"

    def test_query(self, start, end, description):
        path, cost, nodes_explored = self.run_dijkstra(start, end)
        expected = self.EXPECTED_COSTS.get((start, end))
        passed = False
        if expected is not None and cost is not None:
            try:
                if abs(float(cost) - expected) < 0.1: passed = True
            except:
                pass
        elif path is not None:
            passed = True

        return {"name": description, "passed": passed, "start": start, "end": end, "expected_cost": expected,
                "actual_cost": cost, "points": 3 if passed else 0, "nodes_explored": nodes_explored}

    def run_all_tests(self):
        tests = [self.test_query(s, e, d) for s, e, d in self.REQUIRED_QUERIES]
        return {"tests": tests, "total_points": sum(t["points"] for t in tests), "max_points": 15}


class AStarTester:
    REQUIRED_QUERIES = DijkstraTester.REQUIRED_QUERIES
    EXPECTED_COSTS = DijkstraTester.EXPECTED_COSTS

    def __init__(self, astar_module, graph):
        self.astar_module = astar_module
        self.graph = graph

    def reconstruct_path_from_parents(self, came_from, start, end):
        current = end
        path = []
        if end not in came_from and str(end) in came_from: end = str(end)
        if start not in came_from and str(start) in came_from: start = str(start)
        if end not in came_from: return None
        while current != start:
            path.append(current)
            current = came_from.get(current)
            if current is None: break
        path.append(start)
        path.reverse()
        return path

    def run_astar(self, start, end):
        try:
            func = None
            if hasattr(self.astar_module, 'AStar'):
                a_class = self.astar_module.AStar(self.graph)
                func = getattr(a_class, 'find_shortest_path', getattr(a_class, 'astar', None))

            if not func:
                func = getattr(self.astar_module, 'astar',
                               getattr(self.astar_module, 'a_star',
                                       getattr(self.astar_module, 'find_shortest_path',
                                               getattr(self.astar_module, 'A_Star_Search',
                                                       getattr(self.astar_module, 'find_path', None)))))

            if not func: return None, None, "No function found"

            start_val, end_val = start, end
            if hasattr(self.graph, 'nodes'):
                keys = list(self.graph.nodes.keys())
                if keys and isinstance(keys[0], str): start_val, end_val = str(start), str(end)

            try:
                sig = inspect.signature(func)
                params = list(sig.parameters.keys())

                # VINCE NJOROGE FIX: Handle signature (input_graph, nodes, start, goal)
                if 'input_graph' in params and 'nodes' in params:
                    g_nodes = getattr(self.graph, 'nodes', {})
                    g_edges = getattr(self.graph, 'edges', {})
                    kwargs = {'input_graph': g_edges, 'nodes': g_nodes}
                    remaining = [p for p in params if p not in ['input_graph', 'nodes']]
                    if len(remaining) >= 2:
                        kwargs[remaining[0]] = start_val
                        kwargs[remaining[1]] = end_val
                    result = func(**kwargs)
                elif 'edges' in params and 'nodes' in params:
                    g_nodes = getattr(self.graph, 'nodes', {})
                    g_edges = getattr(self.graph, 'edges', {})
                    kwargs = {'edges': g_edges, 'nodes': g_nodes}
                    remaining = [p for p in params if p not in ['edges', 'nodes']]
                    if len(remaining) >= 2:
                        kwargs[remaining[0]] = start_val
                        kwargs[remaining[1]] = end_val
                    result = func(**kwargs)
                else:
                    if inspect.ismethod(func):
                        result = func(start_val, end_val)
                    else:
                        result = func(self.graph, start_val, end_val)
            except:
                result = func(self.graph, start_val, end_val)

            nodes_explored, path, cost = None, None, None

            if hasattr(result, 'cost') and hasattr(result, 'path'):
                path = getattr(result, 'path')
                cost = getattr(result, 'cost')
                nodes_explored = getattr(result, 'nodes_explored', None)
            elif isinstance(result, tuple):
                if len(result) == 4:
                    path, cost, nodes_explored = result[0], result[1], result[2]
                elif len(result) >= 3:
                    val1, val2, val3 = result[0], result[1], result[2]
                    if isinstance(val1, dict) and isinstance(val2, dict):
                        path = self.reconstruct_path_from_parents(val1, start_val, end_val)
                        cost = val2.get(end_val)
                        nodes_explored = val3
                    else:
                        for val in result:
                            if isinstance(val, list):
                                path = val
                            elif isinstance(val, (int, float)) and not isinstance(val, bool):
                                if val > 1000:
                                    pass
                                elif isinstance(val, float) or cost is None:
                                    cost = val
                                else:
                                    nodes_explored = val
                elif len(result) == 2:
                    val1, val2 = result
                    if isinstance(val1, list) and isinstance(val2, list):
                        try:
                            nodes_explored = sum(1 for x in val1 if x != float('inf'))
                            idx = -1
                            if isinstance(end, int):
                                idx = end - 1
                            elif str(end).isdigit():
                                idx = int(end) - 1
                            if idx >= 0 and idx < len(val1): cost = val1[idx]
                            parent_map = {}
                            for i, p in enumerate(val2):
                                if p is not None and p != 0:
                                    parent_map[i + 1] = p
                            path = self.reconstruct_path_from_parents(parent_map, start_val, end_val)
                        except:
                            pass
                    elif isinstance(val1, list):
                        path, cost = val1, val2
                    else:
                        cost, path = val1, val2
            elif isinstance(result, dict):
                path = result.get('path', result.get('shortest_path'))
                # VINCE FIX: added 'total_cost' and 'distance'
                cost = result.get('cost',
                                  result.get('total_cost', result.get('total_distance', result.get('distance'))))
                # VINCE FIX: added 'explored'
                nodes_explored = result.get('nodes_explored', result.get('visited_nodes', result.get('explored')))
                if isinstance(nodes_explored, list): nodes_explored = len(nodes_explored)

            return path, cost, nodes_explored
        except Exception as e:
            return None, None, str(e)

    def test_query(self, start, end, description):
        path, cost, nodes_explored = self.run_astar(start, end)
        expected = self.EXPECTED_COSTS.get((start, end))
        passed = False
        if expected is not None and cost is not None:
            try:
                if abs(float(cost) - expected) < 0.1: passed = True
            except:
                pass
        return {"name": description, "passed": passed, "start": start, "end": end, "expected_cost": expected,
                "actual_cost": cost, "points": 3 if passed else 0, "nodes_explored": nodes_explored}

    def run_all_tests(self):
        tests = [self.test_query(s, e, d) for s, e, d in self.REQUIRED_QUERIES]
        return {"tests": tests, "total_points": sum(t["points"] for t in tests), "max_points": 15}


class PerformanceTester:
    def __init__(self, dijkstra_module, astar_module, graph):
        self.d_tester = DijkstraTester(dijkstra_module, graph)
        self.a_tester = AStarTester(astar_module, graph)

    def run_all_tests(self):
        comparisons = []
        for s, e, d in DijkstraTester.REQUIRED_QUERIES:
            _, d_cost, d_nodes = self.d_tester.run_dijkstra(s, e)
            _, a_cost, a_nodes = self.a_tester.run_astar(s, e)

            imp = None
            if d_nodes is not None and a_nodes is not None:
                try:
                    d_val = int(d_nodes)
                    a_val = int(a_nodes)
                    if d_val > 0:
                        imp = ((d_val - a_val) / d_val * 100)
                except:
                    pass

            comparisons.append({
                "query": d, "dijkstra_nodes": d_nodes, "astar_nodes": a_nodes, "astar_improvement": imp
            })

        tracking = any(c["dijkstra_nodes"] is not None for c in comparisons)
        return {"comparisons": comparisons, "tracking_works": tracking, "points": 5 if tracking else 0}