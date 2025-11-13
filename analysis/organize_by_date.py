#!/usr/bin/env python3
"""
Organize email files by date.
Creates year/month/day hierarchy and copies emails to appropriate folders.
Uses first date found in file if multiple dates exist.
"""

import os
import re
from datetime import datetime
from pathlib import Path
import shutil

# Paths
email_dir = '../TEXT_sorted/email'
output_base = 'byDate'

# Date patterns to match
date_patterns = [
    # Sent: 4/5/2018 10:16:55 PM
    (r'Sent:\s*(\d{1,2})/(\d{1,2})/(\d{4})', '%m/%d/%Y'),
    # Date: Fri, Mar 18, 2016 at 11:39 AM
    (r'Date:\s*[A-Za-z]+,\s*([A-Za-z]+)\s+(\d{1,2}),\s*(\d{4})', '%B %d %Y'),
    # Date: April 27, 2016 at 3:47:49 PM EDT
    (r'Date:\s*([A-Za-z]+)\s+(\d{1,2}),\s*(\d{4})', '%B %d %Y'),
    # Sent: Friday, March 18, 2016 11:41 AM
    (r'Sent:\s*[A-Za-z]+,\s*([A-Za-z]+)\s+(\d{1,2}),\s*(\d{4})', '%B %d %Y'),
]

month_map = {
    'Jan': 'January', 'Feb': 'February', 'Mar': 'March', 'Apr': 'April',
    'May': 'May', 'Jun': 'June', 'Jul': 'July', 'Aug': 'August',
    'Sep': 'September', 'Oct': 'October', 'Nov': 'November', 'Dec': 'December'
}

def parse_date_from_file(filepath):
    """Extract first date from email file."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
            # Try each pattern
            for pattern, date_format in date_patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    try:
                        if date_format == '%m/%d/%Y':
                            # Pattern: Sent: 4/5/2018
                            month, day, year = match.groups()
                            date_str = f"{month}/{day}/{year}"
                            return datetime.strptime(date_str, '%m/%d/%Y')
                        elif date_format == '%B %d %Y':
                            # Pattern: Date: Fri, Mar 18, 2016 or Date: April 27, 2016
                            month_name, day, year = match.groups()
                            # Handle abbreviated months
                            if month_name in month_map:
                                month_name = month_map[month_name]
                            date_str = f"{month_name} {day} {year}"
                            return datetime.strptime(date_str, '%B %d %Y')
                    except (ValueError, IndexError):
                        continue
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    
    return None

def main():
    # Count files before
    email_files = [f for f in os.listdir(email_dir) if f.endswith('.txt')]
    before_count = len(email_files)
    print(f"Total email files: {before_count}")
    
    # Track statistics
    files_with_dates = 0
    files_without_dates = 0
    date_errors = []
    
    # Process each email file
    for filename in email_files:
        filepath = os.path.join(email_dir, filename)
        date = parse_date_from_file(filepath)
        
        if date:
            # Create directory structure: year/month/day
            year = str(date.year)
            month = f"{date.month:02d}"
            day = f"{date.day:02d}"
            
            target_dir = os.path.join(output_base, year, month, day)
            os.makedirs(target_dir, exist_ok=True)
            
            # Copy file to target directory
            target_path = os.path.join(target_dir, filename)
            shutil.copy2(filepath, target_path)
            
            files_with_dates += 1
        else:
            # No date found - put in "no_date" folder
            no_date_dir = os.path.join(output_base, 'no_date')
            os.makedirs(no_date_dir, exist_ok=True)
            target_path = os.path.join(no_date_dir, filename)
            shutil.copy2(filepath, target_path)
            
            files_without_dates += 1
            date_errors.append(filename)
    
    # Count files after
    after_count = sum(len(files) for r, d, files in os.walk(output_base))
    
    print(f"\n=== Results ===")
    print(f"Files with dates: {files_with_dates}")
    print(f"Files without dates: {files_without_dates}")
    print(f"Before count: {before_count}")
    print(f"After count: {after_count}")
    print(f"Match: {before_count == after_count}")
    
    if files_without_dates > 0:
        print(f"\nFirst 10 files without dates:")
        for f in date_errors[:10]:
            print(f"  {f}")

if __name__ == '__main__':
    main()

