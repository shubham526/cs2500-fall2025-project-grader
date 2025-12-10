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

    def __init__(self, submissions_file=None, output_dir="grading_reports", dataset_dir=None):
        self.submissions_file = submissions_file
        self.output_dir = output_dir
        self.dataset_dir = dataset_dir
        self.results = []

        # Validate submissions file exists (if provided)
        if submissions_file and not os.path.exists(submissions_file):
            raise FileNotFoundError(f"Submissions file not found: {submissions_file}")

        # Validate dataset directory (if provided)
        if dataset_dir:
            if not os.path.exists(dataset_dir):
                raise FileNotFoundError(f"Dataset directory not found: {dataset_dir}")
            nodes_csv = os.path.join(dataset_dir, "nodes.csv")
            edges_csv = os.path.join(dataset_dir, "edges.csv")
            if not os.path.exists(nodes_csv):
                raise FileNotFoundError(f"nodes.csv not found in dataset directory: {nodes_csv}")
            if not os.path.exists(edges_csv):
                raise FileNotFoundError(f"edges.csv not found in dataset directory: {edges_csv}")

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
            "max_automated_score": 52,  # Adjusted to 52 (feature is now manual)
            "errors": []
        }

        # If dataset directory provided, copy CSV files to student repo
        if self.dataset_dir:
            print(f"\nUsing shared dataset from: {self.dataset_dir}")
            try:
                src_nodes = os.path.join(self.dataset_dir, "nodes.csv")
                src_edges = os.path.join(self.dataset_dir, "edges.csv")
                dst_nodes = os.path.join(repo_dir, "nodes.csv")
                dst_edges = os.path.join(repo_dir, "edges.csv")

                shutil.copy2(src_nodes, dst_nodes)
                shutil.copy2(src_edges, dst_edges)
                print(f"  ✓ Copied nodes.csv and edges.csv to student repo")
            except Exception as e:
                results["errors"].append(f"Failed to copy dataset: {str(e)}")
                print(f"  ❌ Failed to copy dataset: {str(e)}")
                return results

        # Step 1: Verify required files
        print("\n[1/6] Checking required files...")
        results["files_found"] = self.verify_required_files(repo_dir)

        # Categorize missing files
        critical_files = ["graph.py", "dijkstra.py", "astar.py"]
        optional_files = ["main.py", "DesignDocument.pdf", "README.md", "nodes.csv", "edges.csv"]

        missing_critical = [f for f in critical_files if not results["files_found"].get(f, False)]
        missing_optional = [f for f in optional_files if not results["files_found"].get(f, False)]

        # Only stop if critical Python files are missing
        if missing_critical:
            results["errors"].append(f"Missing critical files: {', '.join(missing_critical)}")
            print(f"  ❌ Missing critical files: {', '.join(missing_critical)}")
            print(f"     Cannot grade without these files.")
            return results

        # Note optional missing files but DO NOT add to errors (preserves execution points)
        if missing_optional:
            flag_msg = f"Missing optional files: {', '.join(missing_optional)}"
            results["flags"].append({"type": "warning", "message": flag_msg})
            print(f"  ⚠️  {flag_msg}")
            print(f"     (Continuing with code grading)")
        else:
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

        # Initialize safe reference
        graph_instance = None

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
            if graph_instance is None:
                raise Exception("Graph could not be built, skipping A* tests")

            astar_tester = AStarTester(astar_module, graph_instance)
            results["astar_tests"] = astar_tester.run_all_tests()

            passed = sum(1 for t in results["astar_tests"]["tests"] if t["passed"])
            total = len(results["astar_tests"]["tests"])
            print(f"  ✓ Passed {passed}/{total} A* tests")

        except Exception as e:
            results["errors"].append(f"A* testing error: {str(e)}")
            print(f"  ❌ A* testing failed: {str(e)}")
            # traceback.print_exc()

        # Step 6: Performance comparison
        print("\n[6/6] Running performance tests...")
        try:
            if graph_instance is None:
                raise Exception("Graph could not be built, skipping performance tests")

            perf_tester = PerformanceTester(dijkstra_module, astar_module, graph_instance)
            results["performance_tests"] = perf_tester.run_all_tests()

            print(f"  ✓ Performance tests complete")

        except Exception as e:
            results["errors"].append(f"Performance testing error: {str(e)}")
            print(f"  ❌ Performance testing failed: {str(e)}")
            # traceback.print_exc()

        # Check for code quality flags
        print("\nChecking code quality flags...")
        results["flags"].extend(self.check_code_flags(repo_dir))

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

        # Code execution: 5 points (clean run with no critical errors)
        if len(results.get("errors", [])) == 0:
            score += 5

        return round(score, 1)

    def grade_single_directory(self, repo_dir, student_name=None):
        """
        Grade a single directory (already cloned repo)

        Args:
            repo_dir: Path to the repository directory
            student_name: Optional student name (defaults to directory name)

        Returns:
            dict: Grading results
        """
        repo_path = Path(repo_dir).resolve()

        if not repo_path.exists():
            print(f"\n❌ Error: Directory not found: {repo_dir}")
            return None

        if not repo_path.is_dir():
            print(f"\n❌ Error: Not a directory: {repo_dir}")
            return None

        # Use directory name as student name if not provided
        if student_name is None:
            student_name = repo_path.name.replace('-', ' ').replace('_', ' ').title()

        print(f"\n{'=' * 60}")
        print(f"Grading: {student_name}")
        print(f"Directory: {repo_path}")
        print(f"{'=' * 60}")

        # Run tests on this directory
        results = self.run_tests_on_submission(str(repo_path), student_name)
        results["repo_url"] = f"Local: {repo_path}"

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

        return results

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
                        "max_automated_score": 52
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
                max_score = result.get("max_automated_score", 52)
                percentage = (score / max_score * 100) if max_score > 0 else 0

                line = f"{student:30s} {score:5.1f}/{max_score} ({percentage:5.1f}%)\n"
                f.write(line)
                print(line.strip())

            f.write("\n" + "=" * 60 + "\n")

            # Statistics
            scores = [r.get("automated_score", 0) for r in self.results]
            avg_score = sum(scores) / len(scores) if scores else 0

            stats = f"\nTotal Submissions: {len(self.results)}\n"
            stats += f"Average Score: {avg_score:.1f}/52\n"
            stats += f"Highest Score: {max(scores) if scores else 0:.1f}/52\n"
            stats += f"Lowest Score: {min(scores) if scores else 0:.1f}/52\n"

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
  # Grade all submissions from file
  python autograder.py -s submissions.txt -o grading_reports

  # Grade a single local directory
  python autograder.py -d /path/to/student/repo -o output_dir

  # Specify dataset location (if not in student repos)
  python autograder.py -d ./student-repo -o reports --dataset /path/to/data

  # Grade with shared dataset for all students
  python autograder.py -s submissions.txt -o reports --dataset ~/cs2500-data
        """
    )

    # Create mutually exclusive group for input methods
    input_group = parser.add_mutually_exclusive_group(required=True)

    input_group.add_argument(
        '-s', '--submissions',
        type=str,
        help='Path to submissions file with format: StudentName,RepoURL'
    )

    input_group.add_argument(
        '-d', '--dir',
        type=str,
        help='Grade a single directory (already cloned repo)'
    )

    parser.add_argument(
        '-n', '--name',
        type=str,
        help='Student name (only used with --dir, optional)'
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        default='grading_reports',
        help='Path to output directory for reports (default: grading_reports/)'
    )

    parser.add_argument(
        '--dataset',
        type=str,
        help='Path to directory containing nodes.csv and edges.csv (if not in student repos)'
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

    # Determine mode
    if args.dir:
        # Single directory mode
        print(f"Mode: Single Directory")
        print(f"  Directory: {os.path.abspath(args.dir)}")
        print(f"  Student: {args.name if args.name else '(auto-detect from directory name)'}")
        print(f"  Output: {os.path.abspath(args.output)}")
        if args.dataset:
            print(f"  Dataset: {os.path.abspath(args.dataset)}")
        print()

        try:
            # Create autograder instance (no submissions file needed)
            autograder = Autograder(
                submissions_file=None,
                output_dir=args.output,
                dataset_dir=args.dataset
            )

            # Grade single directory
            result = autograder.grade_single_directory(args.dir, args.name)

            if result:
                print("\n" + "=" * 60)
                print("GRADING COMPLETE!")
                print("=" * 60)
                print(f"\nAutomated Score: {result['automated_score']}/{result['max_automated_score']}")
                print(f"Report saved to: {os.path.abspath(args.output)}")
            else:
                print("\n❌ Grading failed - see errors above")
                sys.exit(1)

        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            traceback.print_exc()
            sys.exit(1)

    else:
        # Batch mode with submissions file
        print(f"Mode: Batch Grading")
        print(f"  Submissions file: {os.path.abspath(args.submissions)}")
        print(f"  Output directory: {os.path.abspath(args.output)}")
        if args.dataset:
            print(f"  Dataset: {os.path.abspath(args.dataset)}")
        print()

        try:
            # Create autograder instance
            autograder = Autograder(
                submissions_file=args.submissions,
                output_dir=args.output,
                dataset_dir=args.dataset
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