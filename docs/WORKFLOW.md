# Autograder Workflow

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     AUTOGRADER SYSTEM                       │
└─────────────────────────────────────────────────────────────┘

INPUT                    PROCESSING                   OUTPUT
═════                    ══════════════                ══════

submissions.txt    ┌──────────────────────┐
(Student repos) ──→│  autograder.py       │
                   │  - Clone repos       │
                   │  - Load modules      │──→ grading_reports/
                   │  - Run tests         │    ├── Student1_report.pdf
                   └──────────┬───────────┘    ├── Student1_results.json
                              │                 ├── Student2_report.pdf
                              ↓                 ├── Student2_results.json
                   ┌──────────────────────┐    └── grading_summary.txt
                   │  test_suite.py       │
                   │  - GraphTester       │
                   │  - DijkstraTester    │
                   │  - AStarTester       │
                   │  - PerformanceTester │
                   └──────────┬───────────┘
                              │
                              ↓
reference_data/    ┌──────────────────────┐
├── nodes.csv   ──→│  Student Code        │
└── edges.csv      │  - graph.py          │
                   │  - dijkstra.py       │
                   │  - astar.py          │
                   └──────────┬───────────┘
                              │
                              ↓
                   ┌──────────────────────┐
                   │  report_generator.py │
                   │  - Create PDF        │
                   │  - Tables & Charts   │
                   │  - Professional      │
                   │    formatting        │
                   └──────────────────────┘
```

## Processing Flow

```
START
  │
  ├─→ Read submissions.txt
  │
  ├─→ For Each Student:
  │    │
  │    ├─→ Clone GitHub repo
  │    │
  │    ├─→ Verify required files
  │    │    ├── graph.py ✓
  │    │    ├── dijkstra.py ✓
  │    │    ├── astar.py ✓
  │    │    ├── main.py ✓
  │    │    ├── DesignDocument.pdf ✓
  │    │    └── README.md ✓
  │    │
  │    ├─→ Load Python modules
  │    │
  │    ├─→ Run Tests:
  │    │    │
  │    │    ├─→ Graph Operations (12 pts)
  │    │    │    ├── CSV parsing
  │    │    │    ├── Add/remove nodes
  │    │    │    ├── Add/remove edges
  │    │    │    ├── Get neighbors
  │    │    │    └── Get edge weights
  │    │    │
  │    │    ├─→ Dijkstra Tests (15 pts)
  │    │    │    ├── Query 1: 1→14
  │    │    │    ├── Query 2: 8→9
  │    │    │    ├── Query 3: 4→13
  │    │    │    ├── Query 4: 6→10
  │    │    │    └── Query 5: 3→11
  │    │    │
  │    │    ├─→ A* Tests (15 pts)
  │    │    │    ├── Query 1: 1→14
  │    │    │    ├── Query 2: 8→9
  │    │    │    ├── Query 3: 4→13
  │    │    │    ├── Query 4: 6→10
  │    │    │    └── Query 5: 3→11
  │    │    │
  │    │    ├─→ Performance Tests (5 pts)
  │    │    │    └── Node exploration tracking
  │    │    │
  │    │    └─→ Code Execution (5 pts)
  │    │
  │    ├─→ Check Code Quality Flags
  │    │    ├── Priority queue usage
  │    │    ├── Comment density
  │    │    └── Heuristic detection
  │    │
  │    ├─→ Calculate Automated Score
  │    │
  │    ├─→ Generate PDF Report
  │    │
  │    └─→ Save JSON Results
  │
  ├─→ Generate Summary
  │
END
```

## Test Execution Detail

```
For Each Test:
┌──────────────────────────────────────────┐
│ 1. Setup Test Environment               │
│    - Import student code                │
│    - Build graph from CSV               │
└──────────────────┬───────────────────────┘
                   │
┌──────────────────▼───────────────────────┐
│ 2. Execute Test                          │
│    try:                                  │
│        result = student_function(...)    │
│    except Exception as e:                │
│        mark as failed                    │
└──────────────────┬───────────────────────┘
                   │
┌──────────────────▼───────────────────────┐
│ 3. Verify Result                         │
│    - Check path cost matches expected   │
│    - Verify path is valid               │
│    - Count nodes explored               │
└──────────────────┬───────────────────────┘
                   │
┌──────────────────▼───────────────────────┐
│ 4. Record Outcome                        │
│    {                                     │
│      "name": "Query 1",                  │
│      "passed": true,                     │
│      "expected_cost": 42.0,              │
│      "actual_cost": 42.0,                │
│      "nodes_explored": 7,                │
│      "points": 3                         │
│    }                                     │
└──────────────────────────────────────────┘
```

## PDF Report Generation

```
Raw Test Results
      │
      ├─→ Format Tables
      │    ├── File validation table
      │    ├── Graph operations results
      │    ├── Dijkstra results table
      │    ├── A* results table
      │    └── Performance comparison
      │
      ├─→ Create Charts
      │    └── Bar chart: Nodes explored
      │
      ├─→ Add Flags Section
      │    ├── Priority queue warning
      │    ├── Comment density info
      │    └── Heuristic detection
      │
      ├─→ Add Manual Checklist
      │    ├── Code quality items
      │    ├── Proof requirements
      │    ├── Document sections
      │    └── Analysis requirements
      │
      └─→ Generate PDF
           └── Professional_Report.pdf
```

## Grading Workflow

```
INSTRUCTOR WORKFLOW
═══════════════════

Before Semester:
┌────────────────────────────────┐
│ 1. Setup (one-time, 10 min)   │
│    - Install dependencies      │
│    - Calculate expected costs  │
│    - Test with reference impl  │
└────────────────────────────────┘

During Semester:
┌────────────────────────────────┐
│ 2. Share Dataset with Students │
│    - nodes.csv                 │
│    - edges.csv                 │
└────────────────────────────────┘

After Deadline:
┌────────────────────────────────┐
│ 3. Collect Submissions (5 min)│
│    - Get GitHub URLs           │
│    - Add to submissions.txt    │
└───────────┬────────────────────┘
            │
┌───────────▼────────────────────┐
│ 4. Run Autograder (automated)  │
│    python autograder.py        │
│    Time: ~2 min per student    │
└───────────┬────────────────────┘
            │
┌───────────▼────────────────────┐
│ 5. Manual Review (25 min each) │
│    - Check PDF report (2 min)  │
│    - Read design doc (10 min)  │
│    - Review code (8 min)       │
│    - Test extra feature (5 min)│
└───────────┬────────────────────┘
            │
┌───────────▼────────────────────┐
│ 6. Enter Scores (2 min each)   │
│    - Automated: from PDF       │
│    - Manual: from review       │
│    - Total: automated + manual │
└────────────────────────────────┘
```

## Student Perspective

```
STUDENT WORKFLOW
════════════════

┌────────────────────────────────┐
│ 1. Get Dataset Files           │
│    - nodes.csv                 │
│    - edges.csv                 │
└───────────┬────────────────────┘
            │
┌───────────▼────────────────────┐
│ 2. Implement Required Parts    │
│    - graph.py                  │
│    - dijkstra.py               │
│    - astar.py                  │
│    - main.py                   │
│    - Additional feature        │
└───────────┬────────────────────┘
            │
┌───────────▼────────────────────┐
│ 3. Write Design Document       │
│    - Algorithm explanations    │
│    - Proof of correctness      │
│    - Analysis and comparison   │
└───────────┬────────────────────┘
            │
┌───────────▼────────────────────┐
│ 4. Test Locally                │
│    - Run main.py               │
│    - Verify all 5 queries work │
│    - Check additional feature  │
└───────────┬────────────────────┘
            │
┌───────────▼────────────────────┐
│ 5. Submit GitHub URL           │
│    Private repo with instructor│
│    as collaborator             │
└───────────┬────────────────────┘
            │
┌───────────▼────────────────────┐
│ 6. Receive Grading Report      │
│    - Automated score (55 pts)  │
│    - Manual feedback (95 pts)  │
│    - Total bonus calculation   │
└────────────────────────────────┘
```

## Error Handling

```
Error Types:
════════════

Repository Errors:
├── Clone failed → Log error, skip student, generate error report
├── Missing files → Mark missing, run tests on available files
└── Git timeout → Retry once, then skip

Code Errors:
├── Syntax errors → Can't load module, mark as failed
├── Runtime errors → Catch exception, mark test as failed
├── Import errors → Note in report, partial credit for other tests
└── Timeout → Kill process, mark test as timed out

Test Errors:
├── Wrong output format → Try to parse, flag for manual review
├── Missing function → Mark test as failed, suggest function name
├── Invalid result → Compare with expected, show difference
└── No result → Mark as failed with error message

Report Generation Errors:
└── ReportLab error → Generate text report instead, log error
```

## Scoring Algorithm

```
Automated Score Calculation:
════════════════════════════

score = 0

# Graph Operations (12 points)
for test in graph_tests:
    if test.passed:
        score += 2.4  # 12 points / 5 tests

# Dijkstra Correctness (15 points)
for query in dijkstra_queries:
    if correct_cost(query):
        score += 3  # 15 points / 5 queries

# A* Correctness (15 points)
for query in astar_queries:
    if correct_cost(query):
        score += 3  # 15 points / 5 queries

# Performance Tracking (5 points)
if tracks_nodes_explored:
    score += 5

# Additional Feature (3 points)
if feature_detected:
    score += 3

# Code Execution (5 points)
if no_errors:
    score += 5

total_automated = score  # Out of 55
manual_needed = 95       # Requires human review
project_total = 150

# Bonus conversion
bonus = (total_automated + manual_score) / 150 * 20
```

---

## Quick Reference

- **Setup**: `python test_setup.py`
- **Calculate Costs**: `cd reference_implementation && python dijkstra.py`
- **Run Grading**: `python autograder.py`
- **Check Reports**: `ls grading_reports/`

**Time Investment**:
- Setup: 10 min (one-time)
- Per student: 2 min automated + 25 min manual = 27 min total
- **vs. 45 min fully manual = 18 min saved per student**