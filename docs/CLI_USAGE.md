# Command-Line Usage Guide

## Quick Start

### Basic Usage (defaults)
```bash
# From project root
python grade.py

# This uses:
# - submissions.txt (in current directory)
# - grading_reports/ (in current directory)
```

### Specify Submissions File
```bash
python grade.py --submissions /path/to/submissions.txt
# or
python grade.py -s /path/to/submissions.txt
```

### Specify Output Directory
```bash
python grade.py --output /path/to/output/dir
# or
python grade.py -o /path/to/output/dir
```

### Specify Both
```bash
python grade.py -s ~/Desktop/cs2500-submissions.txt -o ~/Documents/grading_reports
```

## Command-Line Options

```
usage: autograder.py [-h] [-s SUBMISSIONS] [-o OUTPUT] [-v]

CS 2500 Extra Credit Project Autograder

optional arguments:
  -h, --help            show this help message and exit
  -s SUBMISSIONS, --submissions SUBMISSIONS
                        Path to submissions file (default: submissions.txt in current directory)
  -o OUTPUT, --output OUTPUT
                        Path to output directory for reports (default: grading_reports/ in current directory)
  -v, --verbose         Enable verbose output
```

## Usage Examples

### Example 1: Default Behavior
```bash
# Everything in current directory
python grade.py
```
- Looks for `submissions.txt` in current directory
- Creates `grading_reports/` in current directory
- Generates reports there

### Example 2: Submissions on Desktop
```bash
python grade.py --submissions ~/Desktop/fall2025-submissions.txt
```
- Uses submissions file from Desktop
- Still outputs to `grading_reports/` in current directory

### Example 3: Output to External Drive
```bash
python grade.py --output /Volumes/ExternalDrive/CS2500_Grading
```
- Uses `submissions.txt` from current directory
- Saves reports to external drive (more secure!)

### Example 4: Both Custom Paths
```bash
python grade.py \
  --submissions ~/Dropbox/Teaching/CS2500/submissions.txt \
  --output ~/Dropbox/Teaching/CS2500/Grading/Fall2025
```
- Submissions from Dropbox
- Reports to Dropbox (can access from anywhere)

### Example 5: Absolute Paths
```bash
python grade.py \
  -s /Users/shubham/Teaching/CS2500/submissions.txt \
  -o /Users/shubham/Teaching/CS2500/Reports
```

### Example 6: Keep Reports Private (outside repo)
```bash
python grade.py \
  -s submissions.txt \
  -o ~/private_grading_reports
```
- Submissions in repo (tracked in git)
- Reports outside repo (not tracked, stays private)

## Recommended Workflows

### Workflow 1: Keep Everything Private
```bash
# Store submissions outside the repo
python grade.py \
  -s ~/secure_location/submissions.txt \
  -o ~/secure_location/reports

# Repo stays clean, no student data in git
```

### Workflow 2: Submissions in Repo, Reports Outside
```bash
# Track submissions in git, but keep reports private
python grade.py \
  -s submissions.txt \
  -o ~/private_reports

# Add to .gitignore:
# ~/private_reports/
```

### Workflow 3: Multiple Sections
```bash
# Section A
python grade.py \
  -s submissions_section_a.txt \
  -o reports/section_a

# Section B
python grade.py \
  -s submissions_section_b.txt \
  -o reports/section_b
```

### Workflow 4: Test Run First
```bash
# Test with one submission
python grade.py \
  -s test_submission.txt \
  -o test_output

# Check test_output/report.pdf
# If good, run on all submissions
python grade.py \
  -s all_submissions.txt \
  -o grading_reports
```

## PyCharm Run Configuration

### Method 1: Run grade.py from Project Root
1. Right-click `grade.py` → "Run 'grade'"
2. Or click the green play button next to `if __name__ == "__main__"`

### Method 2: Create Custom Run Configuration
1. Run → Edit Configurations
2. Click + → Python
3. Set:
   - Name: "Grade All"
   - Script path: `/path/to/cs2500-fall2025-project-grader/grade.py`
   - Parameters: `-s submissions.txt -o grading_reports`
   - Working directory: `/path/to/cs2500-fall2025-project-grader`
4. Click OK

Now you can run with the green play button and it uses your custom paths!

### Method 3: Multiple Configurations for Different Scenarios
Create separate run configs:

**"Grade Test"**
- Parameters: `-s test_submission.txt -o test_output`

**"Grade Section A"**
- Parameters: `-s submissions_a.txt -o reports/section_a`

**"Grade All"**
- Parameters: `-s all_submissions.txt -o reports/all`

## Running from Different Directories

### From Project Root
```bash
cd cs2500-fall2025-project-grader
python grade.py -s submissions.txt -o grading_reports
```

### From src/core/ (direct)
```bash
cd cs2500-fall2025-project-grader/src/core
python autograder.py -s ../../submissions.txt -o ../../grading_reports
```

### From Anywhere (absolute paths)
```bash
python /path/to/cs2500-fall2025-project-grader/grade.py \
  -s /path/to/submissions.txt \
  -o /path/to/output
```

## Help Command

```bash
python grade.py --help
# or
python grade.py -h
```

Output:
```
CS 2500 Extra Credit Project Autograder

optional arguments:
  -h, --help            show this help message and exit
  -s SUBMISSIONS, --submissions SUBMISSIONS
                        Path to submissions file (default: submissions.txt)
  -o OUTPUT, --output OUTPUT
                        Path to output directory (default: grading_reports/)
  -v, --verbose         Enable verbose output

Examples:
  # Use defaults
  python autograder.py
  
  # Specify submissions file
  python autograder.py -s /path/to/submissions.txt
  
  # Specify both
  python autograder.py -s ~/submissions.txt -o ~/output
```

## Error Messages

### Submissions File Not Found
```
❌ Error: Submissions file not found: submissions.txt

Please create the submissions file or specify a different path:
  python autograder.py --submissions /path/to/your/submissions.txt
```

**Solution**: Create the file or use correct path

### Output Directory Permission Error
```
❌ Error: Permission denied: /restricted/path/
```

**Solution**: Use a directory where you have write permissions

## Tips

### Tip 1: Use Tab Completion
```bash
python grade.py -s <TAB>
# Your shell will auto-complete file paths
```

### Tip 2: Use Relative Paths for Portability
```bash
# Good - works if you move the repo
python grade.py -s submissions.txt -o reports

# Less portable - breaks if you move the repo
python grade.py -s /Users/shubham/cs2500/submissions.txt
```

### Tip 3: Keep Submissions in Repo, Reports Outside
```bash
# Submissions tracked in git
python grade.py -s submissions.txt -o ~/private_reports

# Add to .gitignore:
~/private_reports/
grading_reports/
```

### Tip 4: Create Bash Aliases
```bash
# In ~/.bashrc or ~/.zshrc
alias grade-cs2500="python ~/cs2500-grader/grade.py -s ~/cs2500-grader/submissions.txt -o ~/Grading/CS2500"

# Then just run:
grade-cs2500
```

### Tip 5: Use Environment Variables
```bash
# Set environment variables
export CS2500_SUBMISSIONS="$HOME/Teaching/submissions.txt"
export CS2500_OUTPUT="$HOME/Teaching/reports"

# Create wrapper script
python grade.py -s "$CS2500_SUBMISSIONS" -o "$CS2500_OUTPUT"
```

## Output Structure

After running, your output directory will contain:

```
grading_reports/  (or your specified directory)
├── John_Doe_report.pdf
├── John_Doe_results.json
├── Jane_Smith_report.pdf
├── Jane_Smith_results.json
├── Bob_Johnson_report.pdf
├── Bob_Johnson_results.json
└── grading_summary.txt
```

## Security Best Practices

1. **Never commit reports to git**
   - Add output directory to `.gitignore`
   - Or use output directory outside the repo

2. **Use absolute paths for sensitive data**
   ```bash
   python grade.py \
     -s ~/secure/submissions.txt \
     -o ~/secure/reports
   ```

3. **Restrict output directory permissions**
   ```bash
   mkdir -p ~/private_grading
   chmod 700 ~/private_grading
   python grade.py -o ~/private_grading
   ```

## Troubleshooting

### "No such file or directory"
- Check your paths are correct
- Use absolute paths if relative paths aren't working
- Check current working directory: `pwd`

### "Permission denied"
- Make sure you own the output directory
- Try a different output location
- Check file permissions: `ls -la`

### Module import errors
- Make sure you're running from project root
- Use the `grade.py` launcher script
- Or run: `PYTHONPATH=src/core python src/core/autograder.py`

## Summary

**Simple usage:**
```bash
python grade.py
```

**Custom paths:**
```bash
python grade.py -s /path/to/submissions.txt -o /path/to/output
```

**Get help:**
```bash
python grade.py --help
```

That's it! No config files needed. 🎉
