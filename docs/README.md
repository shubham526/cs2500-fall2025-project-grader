# CS 2500 Extra Credit Project Autograder

Automated testing and grading system for the Route Planning & Navigation System project.

## Overview

This autograder automates ~55 out of 150 points for the extra credit project, focusing on:
- Graph operations correctness (12 points)
- Dijkstra's algorithm correctness (15 points)  
- A* algorithm correctness (15 points)
- Performance tracking (5 points)
- Additional feature detection (3 points)
- Code execution (5 points)

The remaining ~95 points require manual review (proofs, analysis, design document, code quality).

## Features

✅ **Automated Testing**: Comprehensive test suite for graph operations and pathfinding algorithms

✅ **PDF Reports**: Professional grading reports with tables, charts, and detailed feedback

✅ **Batch Processing**: Grade multiple submissions automatically

✅ **Error Handling**: Graceful handling of broken code with detailed error messages

✅ **Performance Analysis**: Compare Dijkstra vs A* node exploration

✅ **Code Quality Flags**: Detect missing priority queues, low comment density, etc.

## Installation

### Prerequisites
- Python 3.7 or higher
- Git (for cloning student repositories)

### Setup

1. **Clone or download this autograder**
   ```bash
   cd /path/to/autograder
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare dataset files**
   - Copy `nodes.csv` and `edges.csv` to the `reference_data/` directory
   - These files are provided to students and contain the campus map data

## Usage

### Step 1: Prepare Submissions File

Edit `submissions.txt` and add student submissions:

```
# Format: StudentName,GitHubRepoURL
John Doe,https://github.com/johndoe/cs2500-project
Jane Smith,https://github.com/janesmith/cs2500-extra-credit
Bob Johnson,https://github.com/bjohnson/route-planner
```

### Step 2: Run the Autograder

```bash
python autograder.py
```

The autograder will:
1. Clone each repository
2. Run all automated tests
3. Generate PDF reports
4. Save JSON results
5. Create a grading summary

### Step 3: Review Reports

After grading completes:

```
grading_reports/
├── John_Doe_report.pdf          # Professional PDF report
├── John_Doe_results.json        # Raw test results
├── Jane_Smith_report.pdf
├── Jane_Smith_results.json
└── grading_summary.txt          # Summary of all submissions
```

## Output Files

### PDF Report
Each student receives a comprehensive PDF report containing:
- Automated test results with pass/fail status
- Detailed tables for each algorithm
- Performance comparison charts
- Code quality flags and recommendations
- Checklist of items requiring manual review
- Final automated score

### JSON Results
Raw test data in JSON format for further analysis or custom reporting.

### Grading Summary
Text file with all students' scores sorted by performance.

## Project Structure

```
autograder/
├── autograder.py           # Main orchestration script
├── test_suite.py           # All automated tests
├── report_generator.py     # PDF report generation
├── submissions.txt         # List of student repositories
├── requirements.txt        # Python dependencies
├── reference_data/         # Reference dataset files
│   ├── nodes.csv
│   └── edges.csv
├── grading_reports/        # Generated reports (created automatically)
└── README.md              # This file
```

## How Tests Work

### Graph Operations (12 points)
Tests basic graph functionality:
- CSV parsing and loading
- Add/remove nodes
- Add/remove edges
- Get neighbors
- Get edge weights

### Dijkstra's Algorithm (15 points)
Runs 5 required queries and verifies:
- Path cost matches expected optimal cost
- Path is valid (all edges exist)
- Returns correct format

### A* Algorithm (15 points)
Same 5 queries as Dijkstra:
- Verifies optimal path found
- Checks node exploration tracking
- Compares performance vs Dijkstra

### Performance Tracking (5 points)
Verifies both algorithms track `nodes_explored` metric.

## Required Test Queries

The autograder uses these 5 required queries (from project spec):

1. **Query 1 (Long Path)**: Main Gateway (Node 1) → Parking Garage (Node 14)
2. **Query 2 (Short Path)**: Student Center (Node 8) → Cafe (Node 9)
3. **Query 3 (Cross-Map)**: CS Department (Node 4) → Dorm B (Node 13)
4. **Query 4 (Winding Path)**: Physics Building (Node 6) → Gymnasium (Node 10)
5. **Query 5 (Medium Path)**: Library (Node 3) → Aquatic Center (Node 11)

## Expected Costs (Update These!)

⚠️ **IMPORTANT**: You need to calculate the actual optimal costs for your graph dataset and update them in `test_suite.py`:

```python
# In test_suite.py, update these values:
EXPECTED_COSTS = {
    (1, 14): 42.0,   # Update with actual optimal cost
    (8, 9): 5.0,     # Update with actual optimal cost
    (4, 13): 38.0,   # Update with actual optimal cost
    (6, 10): 27.0,   # Update with actual optimal cost
    (3, 11): 31.0    # Update with actual optimal cost
}
```

To find optimal costs:
1. Create a reference implementation of Dijkstra's algorithm
2. Run it on your actual graph data
3. Record the shortest path costs
4. Update the `EXPECTED_COSTS` dictionary

## Customization

### Adjusting Point Values
Edit the scoring in `autograder.py` in the `calculate_score()` method:

```python
def calculate_score(self, results):
    score = 0
    
    # Graph operations: 12 points (adjust multiplier)
    graph_passed = sum(1 for t in results["graph_tests"]["tests"] if t["passed"])
    score += graph_passed * 2.4  # 2.4 points per test
    
    # Dijkstra: 15 points (adjust multiplier)
    dijkstra_passed = sum(1 for t in results["dijkstra_tests"]["tests"] if t["passed"])
    score += dijkstra_passed * 3  # 3 points per test
    
    # ... etc
```

### Adding More Tests
Add new test methods to the appropriate tester class in `test_suite.py`:

```python
class GraphTester:
    def test_new_feature(self):
        # Your test logic here
        return {
            "name": "New Test",
            "passed": True,
            "expected": "...",
            "actual": "...",
            "points": 5
        }
```

### Modifying PDF Layout
Edit `report_generator.py` to customize the PDF report appearance.

## Troubleshooting

### "Module not found" errors
```bash
pip install --upgrade reportlab
```

### Git clone failures
- Check that student repositories are public or you have collaborator access
- Verify URLs in submissions.txt are correct
- Ensure git is installed: `git --version`

### Import errors when loading student code
- Student may have syntax errors
- Student may not have followed required file naming
- Check the error details in the PDF report

### Tests timing out
- Increase timeout values in `autograder.py`
- Some student implementations may be inefficient

## Manual Grading Workflow

After running the autograder:

1. **Review PDF reports** (~25 min per student)
   - Check automated test results
   - Note any flags or warnings

2. **Read design documents** (20 points)
   - Proof of correctness for Dijkstra
   - A* heuristic admissibility explanation
   - Analysis insights and conclusions

3. **Review code quality** (10 points)
   - Priority queue implementation
   - Code organization and comments
   - Best practices

4. **Verify additional features** (7 points)
   - Test the feature manually
   - Assess implementation quality

5. **Enter scores in gradebook**
   - Automated score: from PDF report
   - Manual score: from your review
   - Total = automated + manual

## Scoring Conversion

The project is worth 150 total points, which converts to +20 bonus points:

```
Bonus Points = (Total Score / 150) × 20

Examples:
- 150/150 (100%) → +20.0 points
- 135/150 (90%)  → +18.0 points
- 120/150 (80%)  → +16.0 points
- 105/150 (70%)  → +14.0 points
- 75/150 (50%)   → +10.0 points
```

Minimum threshold: 75/150 (50%) to receive any bonus.

## Time Savings

**Without autograder**: ~45 min per student
- 15 min: Run code and test functionality
- 10 min: Check algorithm correctness
- 20 min: Read document and grade remaining items

**With autograder**: ~25 min per student
- 2 min: Automated testing (hands-off)
- 5 min: Review automated report
- 18 min: Manual grading (document, code quality, analysis)

**Savings**: ~20 minutes per student
For 30 students: **10 hours saved**

## Support

For issues or questions:
1. Check this README
2. Review the code comments
3. Contact the course instructor

## License

This autograder is for educational use in CS 2500 at Missouri S&T.

---

**Version**: 1.0  
**Last Updated**: December 2025  
**Created by**: Shubham Chatterjee