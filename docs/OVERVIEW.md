# CS 2500 Extra Credit Project - Autograder Package

## 📦 What You've Received

A complete, production-ready autograder system for the Route Planning & Navigation System extra credit project. This system automates ~55/150 points of grading with professional PDF reports.

## 🎯 Quick Stats

- **Grading Time Saved**: ~20 minutes per student
- **For 30 students**: Saves ~10 hours of grading time
- **Points Automated**: 55 out of 150 (37%)
- **Reports Generated**: Professional PDF with tables and charts
- **Setup Time**: 5-10 minutes

## 📁 Package Contents

### Core Autograder Files
```
autograder.py          - Main orchestration script (370 lines)
test_suite.py          - Comprehensive test suite (450 lines)
report_generator.py    - ReportLab PDF generator (400 lines)
requirements.txt       - Python dependencies
submissions.txt        - Template for student repos
```

### Documentation
```
README.md             - Complete usage guide (300+ lines)
QUICKSTART.md         - 5-minute setup guide
test_setup.py         - Verification script
```

### Reference Implementation
```
reference_implementation/
├── graph.py          - Graph data structure
├── dijkstra.py       - Dijkstra's algorithm
├── astar.py          - A* algorithm
└── main.py           - Demo program
```

### Dataset Files
```
reference_data/
├── nodes.csv         - 15 campus locations
└── edges.csv         - Road network edges
```

## 🚀 Getting Started (5 minutes)

### 1. Install Dependencies
```bash
pip install reportlab
```

### 2. Verify Setup
```bash
python test_setup.py
```

### 3. Calculate Expected Costs
```bash
cd reference_implementation
python dijkstra.py
```

Copy the output and update `EXPECTED_COSTS` in `test_suite.py` (around line 180).

### 4. Add Student Submissions
Edit `submissions.txt`:
```
John Doe,https://github.com/johndoe/cs2500-project
Jane Smith,https://github.com/janesmith/cs2500-extra-credit
```

### 5. Run Autograder
```bash
python autograder.py
```

### 6. Review Reports
Check `grading_reports/` folder for PDF reports and summary.

## 📊 What Gets Automated

### ✅ Automated (55 points)
- **Graph Operations** (12 pts) - CSV parsing, add/remove, neighbors, weights
- **Dijkstra Correctness** (15 pts) - 5 required queries with optimal costs
- **A* Correctness** (15 pts) - Same 5 queries, optimal paths
- **Performance Tracking** (5 pts) - Nodes explored metric
- **Additional Feature** (3 pts) - Basic detection
- **Code Execution** (5 pts) - Runs without errors

### 👤 Manual Review Required (95 points)
- Code Quality (10 pts) - Comments, organization, priority queue
- Dijkstra Proof & Trace (15 pts) - Correctness proof, step-by-step trace
- A* Analysis (15 pts) - Heuristic admissibility, explanation
- Design Document (20 pts) - All written sections
- Algorithm Analysis (15 pts) - Insights, conclusions
- Additional Feature Quality (7 pts) - Implementation quality
- Testing Quality (5 pts) - Test suite assessment
- Remaining components (8 pts)

## 📄 PDF Report Features

Each student receives a professional PDF with:

✅ **Student Information** - Name, repo, timestamp

✅ **Automated Score** - Highlighted box with percentage

✅ **File Validation** - Checklist of required files

✅ **Test Results Tables** - Pass/fail for all tests

✅ **Performance Charts** - Bar charts comparing algorithms

✅ **Code Quality Flags** - Priority queue, comments, heuristic

✅ **Manual Review Checklist** - What you still need to grade

✅ **Detailed Feedback** - Specific errors and issues

## 🎨 Sample PDF Report Structure

```
┌─────────────────────────────────────────┐
│  CS 2500 - Extra Credit Project        │
│  Automated Grading Report               │
└─────────────────────────────────────────┘

Student: John Doe
Automated Score: 52/55 (94.5%) ✓

1. FILE VALIDATION
   [Table of required files]

2. GRAPH OPERATIONS (12/12) ✓
   [Test results table]

3. DIJKSTRA'S ALGORITHM (15/15) ✓
   [Query results table]

4. A* ALGORITHM (12/15) ⚠
   [Query results with failures highlighted]

5. PERFORMANCE COMPARISON (5/5) ✓
   [Bar chart + comparison table]

INFORMATIONAL FLAGS
   ⚠ No heapq import detected
   ℹ Low comment density (8%)

MANUAL GRADING REQUIRED (95 points)
   □ Code Quality (10 pts)
   □ Dijkstra Proof (8 pts)
   □ Design Document (20 pts)
   [Complete checklist...]
```

## 🔧 Customization

### Adjust Point Values
Edit `calculate_score()` in `autograder.py`:
```python
score += graph_passed * 2.4  # Change multiplier
```

### Add More Tests
Add methods to test classes in `test_suite.py`:
```python
def test_new_feature(self):
    # Your test logic
    return {"name": "New Test", "passed": True, "points": 5}
```

### Modify PDF Layout
Edit `report_generator.py` to change colors, fonts, tables, etc.

## 📈 Expected Workflow

### Before Deadline
1. ✅ Set up autograder (one time, 10 min)
2. ✅ Share dataset files with students
3. ✅ Calculate expected costs

### After Submissions
1. Collect GitHub URLs (5 min)
2. Run autograder (automated, ~2 min per student)
3. Review PDF reports (25 min per student):
   - Check automated results (2 min)
   - Read design document (10 min)
   - Review code quality (8 min)
   - Test additional feature (5 min)
4. Enter final scores in gradebook (2 min per student)

### Time Comparison

**Without Autograder** (30 students)
- 45 min/student × 30 = **22.5 hours**

**With Autograder** (30 students)
- Setup: 10 min (one time)
- Automated: 2 min/student × 30 = 1 hour (hands-off)
- Manual review: 25 min/student × 30 = 12.5 hours
- **Total: ~13.5 hours** (including setup)

**⏱️ Time Saved: ~9 hours**

## 🛠️ Troubleshooting

### Common Issues

**"No module named reportlab"**
```bash
pip install reportlab
```

**Git clone fails**
- Verify URLs are correct
- Check you have access (private repos need collaborator access)
- Use local paths for testing: `/path/to/local/project`

**Expected costs don't match**
```bash
cd reference_implementation
python dijkstra.py  # Recalculate
```

**Student code won't load**
- Check PDF report for specific error
- This is expected for broken submissions
- They'll get partial credit for what works

## 📚 Documentation

- **README.md** - Complete guide with all features and options
- **QUICKSTART.md** - 5-minute setup walkthrough
- **Code Comments** - Every file is heavily documented
- **This File** - Overview and quick reference

## 🔐 Security Notes

The autograder:
- ✅ Clones repos to temporary directories
- ✅ Runs with normal user permissions (no sudo)
- ✅ Implements timeouts on long operations
- ✅ Handles errors gracefully
- ✅ Cleans up temporary files

⚠️ **Student code runs locally** - standard precaution when testing student submissions

## 💡 Tips for Success

1. **Test First**: Run on the reference implementation before real grading
2. **Calculate Costs**: Update EXPECTED_COSTS before grading
3. **Check Reports**: Review a few PDFs to ensure they look good
4. **Batch Process**: Grade all at once for consistency
5. **Keep Records**: JSON files contain raw data for analysis

## 🎓 Pedagogical Value

This autograder helps students by:
- Providing immediate, consistent feedback
- Identifying specific errors clearly
- Showing performance metrics
- Comparing their results to expected outputs

Students can see **exactly** where they lost points in automated sections.

## 📞 Support

For issues:
1. Check README.md troubleshooting section
2. Review code comments in the scripts
3. Run `python test_setup.py` to diagnose
4. Check QUICKSTART.md for common solutions

## 📄 Files Summary

| File | Lines | Purpose |
|------|-------|---------|
| autograder.py | 370 | Main orchestration |
| test_suite.py | 450 | Test cases |
| report_generator.py | 400 | PDF generation |
| graph.py | 130 | Reference graph |
| dijkstra.py | 120 | Reference Dijkstra |
| astar.py | 130 | Reference A* |
| README.md | 350 | Full documentation |
| QUICKSTART.md | 100 | Setup guide |

**Total: ~2,000 lines of production code + documentation**

## ✨ Features Highlight

✅ **Professional PDF Reports** - Publication-quality with ReportLab

✅ **Comprehensive Testing** - Graph, Dijkstra, A*, performance

✅ **Batch Processing** - Grade 30 students automatically

✅ **Error Handling** - Graceful failures with detailed messages

✅ **Performance Charts** - Visual comparison of algorithms

✅ **Code Quality Checks** - Flags missing priority queues, low comments

✅ **Reference Implementation** - Working code for testing

✅ **Dataset Included** - 15 nodes, 29 edges campus map

✅ **Detailed Documentation** - README, quickstart, inline comments

✅ **Verification Script** - test_setup.py to ensure everything works

## 🎉 Ready to Use

Everything is ready to go! Just:
1. Install reportlab
2. Update expected costs
3. Add student repos
4. Run `python autograder.py`

The autograder will handle the rest and produce professional grading reports.

---

**Built for CS 2500 - Algorithms**
**Missouri University of Science and Technology**
**Fall 2025**