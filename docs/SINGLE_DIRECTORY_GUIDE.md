# Single Directory Grading Guide

## Overview

You can grade repos **one at a time** by manually cloning them first, then running the autograder on the local directory.

## 🎯 Why Grade One at a Time?

- ✅ More control over each submission
- ✅ Review repo structure before grading
- ✅ Test with MST GitLab (git-classes.mst.edu) repos
- ✅ Handle authentication issues manually
- ✅ Keep cloned repos for manual review

## 📝 Two Grading Modes

### Mode 1: Batch Grading (submissions.txt file)
```bash
python grade.py -s submissions.txt -o grading_reports
```
- Grades all submissions at once
- Auto-clones from GitHub/GitLab
- Good for large batches of GitHub repos

### Mode 2: Single Directory Grading (one at a time)
```bash
python grade.py -d /path/to/cloned/repo -o grading_reports
```
- Grade one pre-cloned repo
- You handle git clone separately
- Good for MST GitLab, manual review, or testing

## 🚀 Single Directory Workflow

### Step 1: Clone the Student's Repo
```bash
# Clone manually (handles authentication yourself)
cd ~/cs2500-repos
git clone https://git-classes.mst.edu/jdoe/cs2500-project
```

### Step 2: Grade the Cloned Directory
```bash
# Basic (auto-detect student name from folder name)
python grade.py -d ~/cs2500-repos/cs2500-project -o reports

# With explicit student name
python grade.py -d ~/cs2500-repos/cs2500-project -n "John Doe" -o reports

# Relative paths work too
cd ~/cs2500-repos
python /path/to/grade.py -d ./cs2500-project -o ~/reports
```

### Step 3: Review the Report
```bash
open reports/John_Doe_report.pdf
```

## 💡 Examples

### Example 1: MST GitLab Student
```bash
# Clone from MST GitLab
git clone https://git-classes.mst.edu/jdoe/cs2500-extra-credit

# Grade it
python grade.py -d jdoe-cs2500-extra-credit -n "John Doe" -o reports

# Report: reports/John_Doe_report.pdf
```

### Example 2: GitHub Student
```bash
# Clone from GitHub
git clone https://github.com/jsmith/route-planner

# Grade it (name auto-detected as "Route Planner")
python grade.py -d route-planner -o reports

# Or with explicit name
python grade.py -d route-planner -n "Jane Smith" -o reports
```

### Example 3: Grade Multiple Students One-by-One
```bash
# Clone all repos first
cd ~/cs2500-submissions
git clone https://git-classes.mst.edu/student1/project1
git clone https://git-classes.mst.edu/student2/project2
git clone https://github.com/student3/project3

# Grade them one at a time
python ~/grade.py -d project1 -n "Student One" -o ~/reports
python ~/grade.py -d project2 -n "Student Two" -o ~/reports
python ~/grade.py -d project3 -n "Student Three" -o ~/reports

# All reports in ~/reports/
```

### Example 4: Test Your Reference Implementation
```bash
# Grade your own reference implementation
python grade.py -d src/reference_implementation -n "Reference" -o test_output

# Should get perfect score!
```

## 📋 Command-Line Options for Single Directory Mode

```bash
python grade.py -d <directory> [options]

Required:
  -d, --dir PATH        Path to student's cloned repo directory

Optional:
  -n, --name "Name"     Student name (default: auto-detect from folder)
  -o, --output PATH     Output directory (default: grading_reports/)
```

## 🔄 Complete Workflow Example

```bash
# Create a working directory
mkdir ~/cs2500-grading
cd ~/cs2500-grading

# Clone student repos as you receive them
git clone https://git-classes.mst.edu/abc123/project student1-project
git clone https://git-classes.mst.edu/xyz789/project student2-project

# Grade first student
python ~/autograder/grade.py \
  -d student1-project \
  -n "Alice Brown" \
  -o reports

# Output: reports/Alice_Brown_report.pdf

# Grade second student  
python ~/autograder/grade.py \
  -d student2-project \
  -n "Bob Chen" \
  -o reports

# Output: reports/Bob_Chen_report.pdf

# All reports are in reports/ directory
ls reports/
# Alice_Brown_report.pdf
# Alice_Brown_results.json
# Bob_Chen_report.pdf
# Bob_Chen_results.json
```

## 🎓 When to Use Each Mode

### Use Batch Mode (`-s submissions.txt`) when:
- ✅ All repos are on GitHub (public or you have access)
- ✅ Grading many submissions at once
- ✅ Repos don't need manual inspection first
- ✅ Authentication is straightforward

### Use Single Directory Mode (`-d directory`) when:
- ✅ Repos are on MST GitLab (git-classes.mst.edu)
- ✅ You want to inspect repo structure first
- ✅ Need to handle authentication manually
- ✅ Grading submissions as they come in
- ✅ Student repo has unusual structure
- ✅ Testing or debugging the autograder

## 🔍 Auto-Detected vs Explicit Names

### Auto-Detected (from folder name):
```bash
python grade.py -d john-doe-project -o reports
# Student name: "John Doe Project"
```

The autograder converts folder names:
- `john-doe-project` → "John Doe Project"  
- `cs2500_submission` → "Cs2500 Submission"
- `route-planner` → "Route Planner"

### Explicit Name (recommended):
```bash
python grade.py -d john-doe-project -n "John Doe" -o reports
# Student name: "John Doe"
```

Always better to provide the actual student name!

## 🚨 Common Issues

### Issue: "Directory not found"
```bash
# Check the path is correct
ls ~/cs2500-repos/project1

# Use absolute path if needed
python grade.py -d /Users/shubham/cs2500-repos/project1 -o reports
```

### Issue: "Not a directory"
```bash
# Make sure you're pointing to a directory, not a file
python grade.py -d ~/repos/project  # ✅ directory
python grade.py -d ~/repos/main.py  # ❌ file
```

### Issue: Missing required files
```
✗ graph.py: not found
```
- Student didn't submit required files
- This will be noted in the PDF report
- Manual review needed

## 📊 Output

Same as batch mode:
```
grading_reports/
├── John_Doe_report.pdf          # PDF report
├── John_Doe_results.json        # Raw test results
├── Jane_Smith_report.pdf
└── Jane_Smith_results.json
```

## 🔐 Authentication Benefits

Single directory mode lets YOU handle git authentication:

```bash
# MST GitLab with your credentials
git clone https://git-classes.mst.edu/student/repo
# Enter your MST username/password

# Or use SSH keys
git clone git@git-classes.mst.edu:student/repo.git

# Then grade the cloned directory
python grade.py -d repo -n "Student Name" -o reports
```

No need to embed credentials in the autograder!

## 💾 Keeping Repos vs Deleting

### Keep Repos (Single Directory Mode):
```bash
# Repos stay on disk for manual review
git clone https://...
python grade.py -d repo -n "Student" -o reports
# repo/ still exists for manual grading
```

### Auto-Delete (Batch Mode):
```bash
# Repos auto-deleted after grading
python grade.py -s submissions.txt -o reports
# Temp repos are cleaned up automatically
```

## 🎯 Summary

**Quick one-at-a-time workflow:**
```bash
# 1. Clone
git clone <student-repo-url>

# 2. Grade
python grade.py -d <repo-directory> -n "Student Name" -o reports

# 3. Review
open reports/Student_Name_report.pdf
```

**That's it!** No submissions.txt file needed. 🎉
