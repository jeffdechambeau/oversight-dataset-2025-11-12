#!/usr/bin/env python3
"""
Organize email files by date - improved version with more date formats.
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
no_date_dir = os.path.join(output_base, 'no_date')

# Date patterns to match (in order of preference)
date_patterns = [
    # Sent: 4/5/2018 10:16:55 PM
    (r'Sent:\s*(\d{1,2})/(\d{1,2})/(\d{4})\s+\d+:\d+', '%m/%d/%Y'),
    # Sent: 4/5/2018
    (r'Sent:\s*(\d{1,2})/(\d{1,2})/(\d{4})', '%m/%d/%Y'),
    # Sent 9/28/2012 2:41:02 PM (missing colon)
    (r'Sent\s+(\d{1,2})/(\d{1,2})/(\d{4})\s+\d+:\d+', '%m/%d/%Y'),
    # Date: 07/24/2008 11:49 AM
    (r'Date:\s*(\d{1,2})/(\d{1,2})/(\d{4})\s+\d+:\d+', '%m/%d/%Y'),
    # Date: 07/24/2008
    (r'Date:\s*(\d{1,2})/(\d{1,2})/(\d{4})', '%m/%d/%Y'),
    # Date: Fri, Mar 18, 2016 at 11:39 AM
    (r'Date:\s*[A-Za-z]+,\s*([A-Za-z]+)\s+(\d{1,2}),\s*(\d{4})', '%B %d %Y'),
    # Date: Thursday, January 28 2010 11:21 AM (no comma between day and year)
    (r'Date:\s*[A-Za-z]+day,\s*([A-Za-z]+)\s+(\d{1,2})\s+(\d{4})', '%B %d %Y'),
    # Date: April 27, 2016 at 3:47:49 PM EDT
    (r'Date:\s*([A-Za-z]+)\s+(\d{1,2}),\s*(\d{4})', '%B %d %Y'),
    # Sent: Friday, March 18, 2016 11:41 AM
    (r'Sent:\s*[A-Za-z]+,\s*([A-Za-z]+)\s+(\d{1,2}),\s*(\d{4})', '%B %d %Y'),
    # Thursday, July 24, 2008 11:51:14 AM
    (r'([A-Za-z]+day),\s*([A-Za-z]+)\s+(\d{1,2}),\s*(\d{4})\s+\d+:\d+', '%B %d %Y'),
    # Sunday, April 3 2011 03:49 PM (standalone, no comma between day and year)
    (r'([A-Za-z]+day),\s*([A-Za-z]+)\s+(\d{1,2})\s+(\d{4})\s+\d+:\d+', '%B %d %Y'),
    # May 27, 2008 (standalone date in letter)
    (r'^([A-Za-z]+)\s+(\d{1,2}),\s*(\d{4})', '%B %d %Y'),
    # 12/22/2018 8:21:20 PM (standalone date with time)
    (r'^(\d{1,2})/(\d{1,2})/(\d{4})\s+\d+:\d+', '%m/%d/%Y'),
    # 12/22/2018 (standalone date)
    (r'^(\d{1,2})/(\d{1,2})/(\d{4})', '%m/%d/%Y'),
    # 05/27/2008 12:18 (fax format)
    (r'(\d{2})/(\d{2})/(\d{4})\s+\d{2}:\d{2}', '%m/%d/%Y'),
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
            lines = f.readlines()
            content = ''.join(lines)
            
            # Try each pattern
            for pattern, date_format in date_patterns:
                match = re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
                if match:
                    try:
                        if date_format == '%m/%d/%Y':
                            # Pattern: MM/DD/YYYY
                            groups = match.groups()
                            if len(groups) >= 3:
                                month, day, year = groups[0], groups[1], groups[2]
                                date_str = f"{month}/{day}/{year}"
                                parsed = datetime.strptime(date_str, '%m/%d/%Y')
                                # Validate reasonable date range
                                if 2000 <= parsed.year <= 2025:
                                    return parsed
                        elif date_format == '%B %d %Y':
                            # Pattern: Month Day Year
                            groups = match.groups()
                            if len(groups) >= 3:
                                # Handle day name prefix (e.g., "Thursday, July")
                                if len(groups) == 4:
                                    month_name, day, year = groups[1], groups[2], groups[3]
                                else:
                                    month_name, day, year = groups[0], groups[1], groups[2]
                                
                                # Handle abbreviated months
                                if month_name in month_map:
                                    month_name = month_map[month_name]
                                
                                date_str = f"{month_name} {day} {year}"
                                parsed = datetime.strptime(date_str, '%B %d %Y')
                                # Validate reasonable date range
                                if 2000 <= parsed.year <= 2025:
                                    return parsed
                    except (ValueError, IndexError) as e:
                        continue
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    
    return None

def main():
    # Remove old no_date directory and recreate
    if os.path.exists(no_date_dir):
        shutil.rmtree(no_date_dir)
    os.makedirs(no_date_dir, exist_ok=True)
    
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
            
            # Copy file to target directory (remove from no_date if it was there)
            target_path = os.path.join(target_dir, filename)
            if os.path.exists(target_path):
                os.remove(target_path)
            shutil.copy2(filepath, target_path)
            
            files_with_dates += 1
        else:
            # No date found - put in "no_date" folder
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
            # Show first few lines to debug
            try:
                with open(os.path.join(no_date_dir, f), 'r', encoding='utf-8', errors='ignore') as debug_file:
                    print(f"    First 10 lines:")
                    for i, line in enumerate(debug_file):
                        if i >= 10:
                            break
                        print(f"      {line.strip()[:80]}")
            except:
                pass

if __name__ == '__main__':
    main()

