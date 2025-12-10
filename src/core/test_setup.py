#!/usr/bin/env python3
"""
Test script to verify autograder setup
Run this to make sure everything is configured correctly
"""

import os
import sys
from pathlib import Path


def get_project_root():
    """Get the project root directory"""
    # If running from src/core/, go up two levels
    # If running from project root, stay there
    current = Path(__file__).parent

    # Check if we're in src/core/
    if current.name == 'core' and current.parent.name == 'src':
        return current.parent.parent
    # Check if we're in src/
    elif current.name == 'src':
        return current.parent
    # Otherwise assume we're in project root
    else:
        return current


# Set project root
PROJECT_ROOT = get_project_root()
os.chdir(PROJECT_ROOT)


def check_file(filepath, description):
    """Check if a file exists"""
    full_path = PROJECT_ROOT / filepath
    exists = full_path.exists()
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
        # Add paths to sys.path
        ref_impl_path = PROJECT_ROOT / 'src' / 'reference_implementation'
        sys.path.insert(0, str(ref_impl_path))

        from src.reference_implementation.graph import Graph
        from src.reference_implementation.dijkstra import dijkstra
        from src.reference_implementation.astar import astar

        # Load graph with absolute paths
        nodes_path = PROJECT_ROOT / 'data' / 'nodes.csv'
        edges_path = PROJECT_ROOT / 'data' / 'edges.csv'

        g = Graph()
        g.load_from_csv(str(nodes_path), str(edges_path))

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
    print(f"Project Root: {PROJECT_ROOT}")
    print()

    all_passed = True

    # Check required files
    print("\n[1] Checking Required Files")
    print("-" * 60)

    files_to_check = [
        ("src/core/autograder.py", "Main autograder script"),
        ("src/core/test_suite.py", "Test suite"),
        ("src/core/report_generator.py", "PDF report generator"),
        ("requirements.txt", "Python dependencies"),
        ("data/nodes.csv", "Nodes dataset"),
        ("data/edges.csv", "Edges dataset"),
        ("src/reference_implementation/graph.py", "Reference graph implementation"),
        ("src/reference_implementation/dijkstra.py", "Reference Dijkstra implementation"),
        ("src/reference_implementation/astar.py", "Reference A* implementation"),
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
        # Add core to path
        core_path = PROJECT_ROOT / 'src' / 'core'
        sys.path.insert(0, str(core_path))

        from test_suite import DijkstraTester

        expected_costs = DijkstraTester.EXPECTED_COSTS

        if all(cost == 0 or cost > 1 for cost in expected_costs.values()):
            print("  ⚠ Expected costs may need updating")
            print("  ℹ Run: cd src/reference_implementation && python dijkstra.py")
            print("  ℹ Then update EXPECTED_COSTS in src/core/test_suite.py")
        else:
            print("  ✓ Expected costs are configured")

    except Exception as e:
        print(f"  ✗ Could not check expected costs: {e}")
        all_passed = False

    # Check submissions file (optional - not required in repo)
    print("\n[5] Checking Submissions File (Optional)")
    print("-" * 60)

    try:
        submissions_path = PROJECT_ROOT / "submissions.txt"
        if submissions_path.exists():
            with open(submissions_path, 'r') as f:
                lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]

            if len(lines) == 0:
                print("  ℹ submissions.txt exists but is empty")
                print("  ℹ Add submissions in format: StudentName,https://github.com/user/repo")
            else:
                print(f"  ✓ Found {len(lines)} submission(s) in submissions.txt")
                for line in lines[:3]:  # Show first 3
                    parts = line.split(',')
                    if len(parts) == 2:
                        print(f"    • {parts[0]}")
        else:
            print("  ℹ submissions.txt not found (this is OK)")
            print("  ℹ You'll specify the path when running: python grade.py -s /path/to/submissions.txt")

    except Exception as e:
        print(f"  ⚠ Could not read submissions.txt: {e}")
        print("  ℹ This is OK - you can specify the path at runtime")

    # Create grading_reports directory
    print("\n[6] Checking Output Directory")
    print("-" * 60)

    output_dir = PROJECT_ROOT / "grading_reports"
    if not output_dir.exists():
        output_dir.mkdir(parents=True)
        print(f"  ✓ Created grading_reports/ directory")
    else:
        print(f"  ✓ grading_reports/ directory exists")

    # Final verdict
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ALL CHECKS PASSED!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Update EXPECTED_COSTS in src/core/test_suite.py")
        print("   Run: cd src/reference_implementation && python dijkstra.py")
        print("2. Create submissions.txt (or use any path)")
        print("   Format: StudentName,https://github.com/user/repo")
        print("3. Run: python grade.py -s /path/to/submissions.txt -o output_dir")
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