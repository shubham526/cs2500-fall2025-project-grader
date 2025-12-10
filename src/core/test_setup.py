#!/usr/bin/env python3
"""
Test script to verify autograder setup
Run this to make sure everything is configured correctly
"""

import os
import sys
from pathlib import Path


def check_file(filepath, description):
    """Check if a file exists"""
    exists = os.path.exists(filepath)
    status = "✓" if exists else "✗"
    print(f"  {status} {description}: {filepath}")
    return exists


def check_module(module_name):
    """Check if a Python module can be imported"""
    try:
        __import__(module_name)
        print(f"  ✓ {module_name} can be imported")
        return True
    except ImportError as e:
        print(f"  ✗ {module_name} import failed: {e}")
        return False


def test_reference_implementation():
    """Test that reference implementation works"""
    print("\n[3] Testing Reference Implementation")
    print("-" * 60)

    try:
        sys.path.insert(0, 'reference_implementation')
        from graph import Graph
        from dijkstra import dijkstra
        from astar import astar

        # Load graph
        g = Graph()
        g.load_from_csv("reference_data/nodes.csv", "reference_data/edges.csv")

        print(f"  ✓ Graph loaded: {g.num_nodes()} nodes, {g.num_edges()} edges")

        # Test Dijkstra
        path, cost, nodes = dijkstra(g, 1, 14)
        print(f"  ✓ Dijkstra works: path cost = {cost:.2f}")

        # Test A*
        path, cost, nodes = astar(g, 1, 14)
        print(f"  ✓ A* works: path cost = {cost:.2f}")

        return True

    except Exception as e:
        print(f"  ✗ Reference implementation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all verification tests"""
    print("=" * 60)
    print("CS 2500 Autograder - Setup Verification")
    print("=" * 60)

    all_passed = True

    # Check required files
    print("\n[1] Checking Required Files")
    print("-" * 60)

    files_to_check = [
        ("autograder.py", "Main autograder script"),
        ("test_suite.py", "Test suite"),
        ("report_generator.py", "PDF report generator"),
        ("requirements.txt", "Python dependencies"),
        ("submissions.txt", "Submissions file"),
        ("reference_data/nodes.csv", "Nodes dataset"),
        ("reference_data/edges.csv", "Edges dataset"),
        ("reference_implementation/graph.py", "Reference graph implementation"),
        ("reference_implementation/dijkstra.py", "Reference Dijkstra implementation"),
        ("reference_implementation/astar.py", "Reference A* implementation"),
    ]

    for filepath, description in files_to_check:
        if not check_file(filepath, description):
            all_passed = False

    # Check Python modules
    print("\n[2] Checking Python Dependencies")
    print("-" * 60)

    modules_to_check = [
        "reportlab",
    ]

    for module in modules_to_check:
        if not check_module(module):
            all_passed = False
            print(f"\n  💡 Install with: pip install {module}")

    # Test reference implementation
    if not test_reference_implementation():
        all_passed = False

    # Check expected costs
    print("\n[4] Checking Expected Costs Configuration")
    print("-" * 60)

    try:
        from test_suite import DijkstraTester

        expected_costs = DijkstraTester.EXPECTED_COSTS

        if all(cost == 0 or cost > 1 for cost in expected_costs.values()):
            print("  ⚠ Expected costs may need updating")
            print("  ℹ Run: cd reference_implementation && python dijkstra.py")
            print("  ℹ Then update EXPECTED_COSTS in test_suite.py")
        else:
            print("  ✓ Expected costs are configured")

    except Exception as e:
        print(f"  ✗ Could not check expected costs: {e}")
        all_passed = False

    # Check submissions file
    print("\n[5] Checking Submissions File")
    print("-" * 60)

    try:
        with open("submissions.txt", 'r') as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]

        if len(lines) == 0:
            print("  ℹ No submissions yet (this is OK)")
            print("  ℹ Add submissions in format: StudentName,https://github.com/user/repo")
        else:
            print(f"  ✓ Found {len(lines)} submission(s)")
            for line in lines[:3]:  # Show first 3
                parts = line.split(',')
                if len(parts) == 2:
                    print(f"    • {parts[0]}")

    except Exception as e:
        print(f"  ✗ Could not read submissions.txt: {e}")
        all_passed = False

    # Create grading_reports directory
    print("\n[6] Checking Output Directory")
    print("-" * 60)

    output_dir = "grading_reports"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"  ✓ Created {output_dir}/ directory")
    else:
        print(f"  ✓ {output_dir}/ directory exists")

    # Final verdict
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ALL CHECKS PASSED!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Update EXPECTED_COSTS in test_suite.py")
        print("   Run: cd reference_implementation && python dijkstra.py")
        print("2. Add student submissions to submissions.txt")
        print("3. Run: python autograder.py")
        print("\nSee QUICKSTART.md for detailed instructions.")
    else:
        print("❌ SOME CHECKS FAILED")
        print("=" * 60)
        print("\nPlease fix the issues above before running the autograder.")
        print("See README.md for troubleshooting help.")

    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)