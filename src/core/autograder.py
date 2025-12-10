#!/usr/bin/env python3
"""
CS 2500 Extra Credit Project Autograder
Automated testing and grading for route planning project
"""

import os
import sys
import json
import subprocess
import shutil
import tempfile
import importlib.util
import argparse
from datetime import datetime
from pathlib import Path
import traceback

# Test imports
from test_suite import GraphTester, DijkstraTester, AStarTester, PerformanceTester
from report_generator import generate_pdf_report


class Autograder:
    """Main autograder class that orchestrates the testing process"""

    def __init__(self, submissions_file, output_dir):
        self.submissions_file = submissions_file
        self.output_dir = output_dir
        self.results = []

        # Validate submissions file exists
        if not os.path.exists(submissions_file):
            raise FileNotFoundError(f"Submissions file not found: {submissions_file}")

        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)

    def clone_repository(self, repo_url, dest_dir):
        """Clone a GitHub repository"""
        try:
            # Clean destination if exists
            if os.path.exists(dest_dir):
                shutil.rmtree(dest_dir)

            # Clone repo
            result = subprocess.run(
                ["git", "clone", repo_url, dest_dir],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode != 0:
                return False, f"Git clone failed: {result.stderr}"

            return True, "Repository cloned successfully"
        except subprocess.TimeoutExpired:
            return False, "Git clone timeout (60s)"
        except Exception as e:
            return False, f"Git clone error: {str(e)}"

    def verify_required_files(self, repo_dir):
        """Check if all required files are present"""
        required_files = [
            "graph.py",
            "dijkstra.py",
            "astar.py",
            "main.py",
            "DesignDocument.pdf",
            "README.md",
            "nodes.csv",
            "edges.csv"
        ]

        results = {}
        for filename in required_files:
            filepath = os.path.join(repo_dir, filename)
            results[filename] = os.path.exists(filepath)

        return results

    def load_student_module(self, repo_dir, module_name):
        """Dynamically load a Python module from the student's repo"""
        try:
            module_path = os.path.join(repo_dir, f"{module_name}.py")
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            return module, None
        except Exception as e:
            return None, f"Failed to load {module_name}.py: {str(e)}"

    def run_tests_on_submission(self, repo_dir, student_name):
        """Run all automated tests on a single submission"""
        print(f"\n{'=' * 60}")
        print(f"Grading: {student_name}")
        print(f"{'=' * 60}")

        results = {
            "student_name": student_name,
            "repo_dir": repo_dir,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "files_found": {},
            "graph_tests": {},
            "dijkstra_tests": {},
            "astar_tests": {},
            "performance_tests": {},
            "additional_feature": {},
            "code_execution": {},
            "flags": [],
            "automated_score": 0,
            "max_automated_score": 55,
            "errors": []
        }

        # Step 1: Verify required files
        print("\n[1/6] Checking required files...")
        results["files_found"] = self.verify_required_files(repo_dir)

        missing_files = [f for f, exists in results["files_found"].items() if not exists]
        if missing_files:
            results["errors"].append(f"Missing files: {', '.join(missing_files)}")
            print(f"  ❌ Missing files: {', '.join(missing_files)}")
            return results
        print("  ✓ All required files found")

        # Step 2: Load student modules
        print("\n[2/6] Loading student code...")
        try:
            # Add repo to path
            sys.path.insert(0, repo_dir)

            graph_module, error = self.load_student_module(repo_dir, "graph")
            if error:
                results["errors"].append(error)
                print(f"  ❌ {error}")
                return results

            dijkstra_module, error = self.load_student_module(repo_dir, "dijkstra")
            if error:
                results["errors"].append(error)
                print(f"  ❌ {error}")
                return results

            astar_module, error = self.load_student_module(repo_dir, "astar")
            if error:
                results["errors"].append(error)
                print(f"  ❌ {error}")
                return results

            print("  ✓ All modules loaded successfully")

        except Exception as e:
            results["errors"].append(f"Module loading error: {str(e)}")
            print(f"  ❌ {str(e)}")
            return results

        # Step 3: Test graph operations
        print("\n[3/6] Testing graph operations...")
        try:
            graph_tester = GraphTester(graph_module, repo_dir)
            results["graph_tests"] = graph_tester.run_all_tests()

            passed = sum(1 for t in results["graph_tests"]["tests"] if t["passed"])
            total = len(results["graph_tests"]["tests"])
            print(f"  ✓ Passed {passed}/{total} graph tests")

        except Exception as e:
            results["errors"].append(f"Graph testing error: {str(e)}")
            print(f"  ❌ Graph testing failed: {str(e)}")
            traceback.print_exc()

        # Step 4: Test Dijkstra's algorithm
        print("\n[4/6] Testing Dijkstra's algorithm...")
        try:
            # Need to build graph first
            graph_instance = graph_tester.build_graph()

            dijkstra_tester = DijkstraTester(dijkstra_module, graph_instance)
            results["dijkstra_tests"] = dijkstra_tester.run_all_tests()

            passed = sum(1 for t in results["dijkstra_tests"]["tests"] if t["passed"])
            total = len(results["dijkstra_tests"]["tests"])
            print(f"  ✓ Passed {passed}/{total} Dijkstra tests")

        except Exception as e:
            results["errors"].append(f"Dijkstra testing error: {str(e)}")
            print(f"  ❌ Dijkstra testing failed: {str(e)}")
            traceback.print_exc()

        # Step 5: Test A* algorithm
        print("\n[5/6] Testing A* algorithm...")
        try:
            astar_tester = AStarTester(astar_module, graph_instance)
            results["astar_tests"] = astar_tester.run_all_tests()

            passed = sum(1 for t in results["astar_tests"]["tests"] if t["passed"])
            total = len(results["astar_tests"]["tests"])
            print(f"  ✓ Passed {passed}/{total} A* tests")

        except Exception as e:
            results["errors"].append(f"A* testing error: {str(e)}")
            print(f"  ❌ A* testing failed: {str(e)}")
            traceback.print_exc()

        # Step 6: Performance comparison
        print("\n[6/6] Running performance tests...")
        try:
            perf_tester = PerformanceTester(dijkstra_module, astar_module, graph_instance)
            results["performance_tests"] = perf_tester.run_all_tests()

            print(f"  ✓ Performance tests complete")

        except Exception as e:
            results["errors"].append(f"Performance testing error: {str(e)}")
            print(f"  ❌ Performance testing failed: {str(e)}")
            traceback.print_exc()

        # Check for code quality flags
        print("\nChecking code quality flags...")
        results["flags"] = self.check_code_flags(repo_dir)

        # Calculate automated score
        results["automated_score"] = self.calculate_score(results)

        print(f"\n{'=' * 60}")
        print(f"Automated Score: {results['automated_score']}/{results['max_automated_score']} points")
        print(f"{'=' * 60}")

        return results

    def check_code_flags(self, repo_dir):
        """Check for informational flags (not scored)"""
        flags = []

        # Check for heapq usage in dijkstra.py
        try:
            with open(os.path.join(repo_dir, "dijkstra.py"), 'r') as f:
                dijkstra_code = f.read()
                if 'heapq' not in dijkstra_code and 'PriorityQueue' not in dijkstra_code:
                    flags.append({
                        "type": "warning",
                        "message": "No 'heapq' or 'PriorityQueue' import found in dijkstra.py",
                        "recommendation": "Verify priority queue usage in manual review"
                    })
        except:
            pass

        # Check comment density
        try:
            with open(os.path.join(repo_dir, "graph.py"), 'r') as f:
                lines = f.readlines()
                total_lines = len(lines)
                comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
                comment_ratio = comment_lines / total_lines if total_lines > 0 else 0

                if comment_ratio < 0.10:
                    flags.append({
                        "type": "info",
                        "message": f"Low comment density: {comment_ratio * 100:.1f}%",
                        "recommendation": "Consider adding more explanatory comments"
                    })
        except:
            pass

        # Check for heuristic function in A*
        try:
            with open(os.path.join(repo_dir, "astar.py"), 'r') as f:
                astar_code = f.read()
                if 'euclidean' in astar_code.lower():
                    flags.append({
                        "type": "info",
                        "message": "A* uses Euclidean distance heuristic",
                        "recommendation": "Verify admissibility in manual review"
                    })
        except:
            pass

        return flags

    def calculate_score(self, results):
        """Calculate the automated score"""
        score = 0

        # Graph operations: 12 points (each test worth 2.4 points)
        if "graph_tests" in results and "tests" in results["graph_tests"]:
            graph_passed = sum(1 for t in results["graph_tests"]["tests"] if t["passed"])
            score += graph_passed * 2.4

        # Dijkstra correctness: 15 points (each test worth 3 points)
        if "dijkstra_tests" in results and "tests" in results["dijkstra_tests"]:
            dijkstra_passed = sum(1 for t in results["dijkstra_tests"]["tests"] if t["passed"])
            score += dijkstra_passed * 3

        # A* correctness: 15 points (each test worth 3 points)
        if "astar_tests" in results and "tests" in results["astar_tests"]:
            astar_passed = sum(1 for t in results["astar_tests"]["tests"] if t["passed"])
            score += astar_passed * 3

        # Performance tracking: 5 points
        if "performance_tests" in results and results["performance_tests"].get("tracking_works", False):
            score += 5

        # Additional feature: 3 points (if detected)
        if "additional_feature" in results and results["additional_feature"].get("detected", False):
            score += 3

        # Code execution: 5 points
        if len(results.get("errors", [])) == 0:
            score += 5

        return round(score, 1)

    def grade_all_submissions(self):
        """Grade all submissions from the submissions file"""

        # Read submissions
        if not os.path.exists(self.submissions_file):
            print(f"Error: {self.submissions_file} not found!")
            print("Create a submissions.txt file with format:")
            print("StudentName,https://github.com/username/repo")
            return

        with open(self.submissions_file, 'r') as f:
            submissions = [line.strip() for line in f if line.strip() and not line.startswith('#')]

        print(f"Found {len(submissions)} submissions to grade")

        # Process each submission
        for i, submission_line in enumerate(submissions, 1):
            print(f"\n\n{'#' * 60}")
            print(f"Processing submission {i}/{len(submissions)}")
            print(f"{'#' * 60}")

            try:
                # Parse submission line
                parts = submission_line.split(',')
                if len(parts) != 2:
                    print(f"Error: Invalid format in line: {submission_line}")
                    continue

                student_name = parts[0].strip()
                repo_url = parts[1].strip()

                # Create temp directory for this submission
                temp_dir = tempfile.mkdtemp(prefix=f"cs2500_{student_name}_")

                # Clone repository
                print(f"\nCloning repository...")
                success, message = self.clone_repository(repo_url, temp_dir)

                if not success:
                    print(f"  ❌ {message}")
                    results = {
                        "student_name": student_name,
                        "repo_url": repo_url,
                        "errors": [message],
                        "automated_score": 0,
                        "max_automated_score": 55
                    }
                else:
                    print(f"  ✓ Repository cloned")

                    # Run tests
                    results = self.run_tests_on_submission(temp_dir, student_name)
                    results["repo_url"] = repo_url

                # Generate PDF report
                print(f"\nGenerating PDF report...")
                pdf_path = os.path.join(self.output_dir, f"{student_name.replace(' ', '_')}_report.pdf")
                generate_pdf_report(results, pdf_path)
                print(f"  ✓ Report saved: {pdf_path}")

                # Save JSON results
                json_path = os.path.join(self.output_dir, f"{student_name.replace(' ', '_')}_results.json")
                with open(json_path, 'w') as f:
                    json.dump(results, f, indent=2)

                self.results.append(results)

                # Cleanup
                try:
                    shutil.rmtree(temp_dir)
                except:
                    pass

            except Exception as e:
                print(f"Error processing submission: {str(e)}")
                traceback.print_exc()

        # Generate summary
        self.generate_summary()

    def generate_summary(self):
        """Generate a summary of all grading results"""
        print(f"\n\n{'=' * 60}")
        print("GRADING SUMMARY")
        print(f"{'=' * 60}\n")

        summary_path = os.path.join(self.output_dir, "grading_summary.txt")

        with open(summary_path, 'w') as f:
            f.write("CS 2500 Extra Credit Project - Grading Summary\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")

            for result in sorted(self.results, key=lambda x: x.get("automated_score", 0), reverse=True):
                student = result["student_name"]
                score = result.get("automated_score", 0)
                max_score = result.get("max_automated_score", 55)
                percentage = (score / max_score * 100) if max_score > 0 else 0

                line = f"{student:30s} {score:5.1f}/{max_score} ({percentage:5.1f}%)\n"
                f.write(line)
                print(line.strip())

            f.write("\n" + "=" * 60 + "\n")

            # Statistics
            scores = [r.get("automated_score", 0) for r in self.results]
            avg_score = sum(scores) / len(scores) if scores else 0

            stats = f"\nTotal Submissions: {len(self.results)}\n"
            stats += f"Average Score: {avg_score:.1f}/55\n"
            stats += f"Highest Score: {max(scores) if scores else 0:.1f}/55\n"
            stats += f"Lowest Score: {min(scores) if scores else 0:.1f}/55\n"

            f.write(stats)
            print(stats)

        print(f"\nSummary saved to: {summary_path}")
        print(f"All reports saved to: {self.output_dir}/")


def parse_arguments():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description='CS 2500 Extra Credit Project Autograder',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use defaults (submissions.txt and grading_reports/)
  python autograder.py

  # Specify submissions file only
  python autograder.py -s /path/to/submissions.txt

  # Specify output directory only
  python autograder.py -o /path/to/output

  # Specify both
  python autograder.py -s ~/submissions.txt -o ~/grading_output

  # Full paths
  python autograder.py --submissions /home/user/fall2025/submissions.txt --output /home/user/reports
        """
    )

    parser.add_argument(
        '-s', '--submissions',
        type=str,
        default='submissions.txt',
        help='Path to submissions file (default: submissions.txt in current directory)'
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        default='grading_reports',
        help='Path to output directory for reports (default: grading_reports/ in current directory)'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    return parser.parse_args()


def main():
    """Main entry point"""

    # Parse arguments
    args = parse_arguments()

    print("""
╔══════════════════════════════════════════════════════════╗
║  CS 2500 - Extra Credit Project Autograder              ║
║  Route Planning & Navigation System                      ║
║  Fall 2025                                               ║
╚══════════════════════════════════════════════════════════╝
    """)

    print(f"Configuration:")
    print(f"  Submissions file: {os.path.abspath(args.submissions)}")
    print(f"  Output directory: {os.path.abspath(args.output)}")
    print()

    try:
        # Create autograder instance
        autograder = Autograder(
            submissions_file=args.submissions,
            output_dir=args.output
        )

        # Grade all submissions
        autograder.grade_all_submissions()

        print("\n" + "=" * 60)
        print("GRADING COMPLETE!")
        print("=" * 60)
        print(f"\nReports saved to: {os.path.abspath(args.output)}")

    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print(f"\nPlease create the submissions file or specify a different path:")
        print(f"  python autograder.py --submissions /path/to/your/submissions.txt")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()