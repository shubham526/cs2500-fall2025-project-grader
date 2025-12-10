# Quick Start Guide

## First-Time Setup (5 minutes)

### Step 1: Calculate Expected Costs

Before you can grade student submissions, you need to know the optimal costs for each test query.

```bash
cd reference_implementation
python dijkstra.py
```

This will output something like:

```
EXPECTED COSTS FOR TEST QUERIES:
============================================================
Copy these values to test_suite.py -> EXPECTED_COSTS

EXPECTED_COSTS = {
    (1, 14): 42.5,  # Main Gateway → Parking Garage (Long Path)
    (8, 9): 1.5,    # Student Center → Cafe (Short Path)
    ...
}
```

### Step 2: Update Expected Costs

Open `test_suite.py` and find these lines (around line 180):

```python
# Expected optimal costs (you'll need to update these based on your dataset)
EXPECTED_COSTS = {
    (1, 14): 42.0,  # Update these with actual optimal costs
    (8, 9): 5.0,
    (4, 13): 38.0,
    (6, 10): 27.0,
    (3, 11): 31.0
}
```

Replace with the values from Step 1.

### Step 3: Test the Autograder

Create a test submission to verify everything works:

```bash
# 1. Create a test repository
mkdir test_student
cp reference_implementation/* test_student/
cp reference_data/*.csv test_student/

# 2. Add to submissions.txt
echo "Test Student,/path/to/test_student" >> submissions.txt

# 3. Run autograder
python autograder.py
```

Check `grading_reports/Test_Student_report.pdf` - it should show perfect scores!

### Step 4: Ready for Real Grading

1. Clear submissions.txt (remove test entry)
2. Add real student GitHub URLs
3. Run `python autograder.py`
4. Review PDF reports in `grading_reports/`

## Testing Without Cloning Repos

If you want to test locally without cloning:

```bash
# Use local file paths instead of GitHub URLs
echo "Local Test,/absolute/path/to/local/project" >> submissions.txt
python autograder.py
```

The autograder will skip the git clone step if the path already exists.

## Common Issues

**Issue**: "No module named 'reportlab'"
```bash
pip install reportlab
```

**Issue**: Expected costs don't match
- Run `reference_implementation/dijkstra.py` to recalculate
- Make sure you're using the same nodes.csv and edges.csv as students

**Issue**: Student code won't load
- Check the error in the PDF report
- Student may have syntax errors or different file structure
- This is expected for broken submissions

## What to Check in PDF Reports

✅ **Automated Score**: Out of 55 points

✅ **Test Results**: Which tests passed/failed

✅ **Flags**: Priority queue usage, comment density, etc.

✅ **Manual Review Checklist**: What you still need to grade

## Next Steps

See the main [README.md](README.md) for:
- Detailed usage instructions
- Customization options
- Manual grading workflow
- Troubleshooting guide

---

**Estimated setup time**: 5-10 minutes
**Grading time per student**: ~2 min automated + ~23 min manual = ~25 min total
**Time saved**: ~20 min per student vs. fully manual grading