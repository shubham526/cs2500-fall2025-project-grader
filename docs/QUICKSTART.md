# Quick Start Guide

## First-Time Setup (5 minutes)

### Step 1: Install Dependencies
```bash
pip install reportlab
```

### Step 2: Calculate Expected Costs

Before you can grade student submissions, you need to know the optimal costs for each test query.

```bash
cd src/reference_implementation
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

### Step 3: Update Expected Costs

Open `src/core/test_suite.py` and find these lines (around line 180):

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

Replace with the values from Step 2.

### Step 4: Create Submissions File

Create `submissions.txt` in the project root:

```txt
# Format: StudentName,GitHubURL
John Doe,https://github.com/johndoe/cs2500-project
Jane Smith,https://github.com/janesmith/cs2500-extra-credit
```

### Step 5: Run the Autograder

**Basic usage (defaults):**
```bash
# From project root
python grade.py

# Uses submissions.txt and outputs to grading_reports/
```

**With custom paths:**
```bash
python grade.py \
  --submissions ~/Desktop/submissions.txt \
  --output ~/Documents/grading_reports
```

**Short form:**
```bash
python grade.py -s submissions.txt -o reports
```

### Step 6: Review Reports

Check your output directory for PDF reports:
```bash
ls grading_reports/
# or
ls ~/Documents/grading_reports/  # if you used custom path
```

## Command-Line Options

```bash
# Get help
python grade.py --help

# Specify submissions file
python grade.py --submissions /path/to/submissions.txt

# Specify output directory
python grade.py --output /path/to/output

# Specify both
python grade.py -s submissions.txt -o ~/grading_reports
```

## Testing Without Cloning Repos

Create a test submission to verify everything works:

```bash
# 1. Create test_submission.txt
echo "Test Student,$(pwd)/src/reference_implementation" > test_submission.txt

# 2. Run autograder on test
python grade.py -s test_submission.txt -o test_output

# 3. Check the report
open test_output/Test_Student_report.pdf  # Mac
# or
xdg-open test_output/Test_Student_report.pdf  # Linux
```

The test should show perfect scores since you're grading the reference implementation!

## Ready for Real Grading

1. Clear test files:
   ```bash
   rm test_submission.txt
   rm -rf test_output/
   ```

2. Add real student GitHub URLs to `submissions.txt`

3. Run autograder:
   ```bash
   python grade.py
   ```

4. Review PDF reports in `grading_reports/`

## PyCharm Setup

### Option 1: Run grade.py Directly
1. Right-click `grade.py` in the project explorer
2. Click "Run 'grade'"
3. Done!

### Option 2: Create Run Configuration
1. Run → Edit Configurations
2. Click + → Python
3. Set:
   - Name: "Grade Students"
   - Script path: `[YOUR_PROJECT]/grade.py`
   - Parameters: `-s submissions.txt -o grading_reports`
   - Working directory: `[YOUR_PROJECT]`
4. Click OK
5. Use the green play button to run

## Common Issues

**Issue**: "Submissions file not found"
```bash
# Solution: Specify the correct path
python grade.py --submissions /full/path/to/submissions.txt
```

**Issue**: Expected costs don't match
```bash
# Solution: Recalculate
cd src/reference_implementation
python dijkstra.py
# Copy output to src/core/test_suite.py
```

**Issue**: "No module named reportlab"
```bash
pip install reportlab
```

## Next Steps

See [CLI_USAGE.md](CLI_USAGE.md) for:
- Detailed command-line examples
- Advanced workflows
- PyCharm integration
- Security best practices

See [README.md](README.md) for:
- Complete documentation
- Customization options
- Manual grading workflow

---

**Estimated setup time**: 5-10 minutes  
**Grading time per student**: ~2 min automated + ~23 min manual = ~25 min total  
**Time saved**: ~20 min per student vs. fully manual grading

No config files needed - everything via command line! 🎉