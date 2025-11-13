#!/usr/bin/env python3
"""
Extract names from "To:" lines in email files.
Split on semicolons and commas, clean up names, and organize by frequency.
Each name becomes a file containing the list of files where that name appears.
"""

import os
import re
from collections import defaultdict

# Paths
email_dir = '../TEXT_sorted/email'
output_dir = 'nameByFreq'

# Create output directory
os.makedirs(output_dir, exist_ok=True)

# Track names and which files contain them
name_to_files = defaultdict(set)
name_counts = defaultdict(int)

def clean_name(name):
    """Clean up a name by removing special characters and normalizing."""
    # Remove email addresses (keep just the name part if present)
    # Handle patterns like "Name <email@domain.com>" or "email@domain.com"
    name = re.sub(r'<[^>]+>', '', name)  # Remove <email@domain.com>
    name = re.sub(r'\[[^\]]+\]', '', name)  # Remove [email@domain.com]
    
    # Remove email addresses themselves
    if '@' in name:
        # Try to extract name before email
        parts = name.split('@')
        if len(parts) > 0:
            # Look for name before @
            before_at = parts[0].strip()
            # Check if there's a name part (not just email username)
            if ' ' in before_at or len(before_at) > 20:
                name = before_at
            else:
                # It's just an email, skip it
                return None
    
    # Clean up the name
    name = name.strip()
    
    # Remove trailing/leading underscores and special chars
    name = name.strip('_').strip()
    
    # Remove common prefixes/suffixes
    name = re.sub(r'^(Mr\.|Mrs\.|Ms\.|Dr\.|Prof\.)\s+', '', name, flags=re.IGNORECASE)
    
    # Remove trailing periods, commas, semicolons
    name = name.rstrip('.,;')
    
    # Remove special characters but keep spaces, hyphens, apostrophes, periods
    name = re.sub(r'[^\w\s\-\'\.]', '', name)
    
    # Replace underscores with spaces
    name = name.replace('_', ' ')
    
    # Normalize whitespace
    name = ' '.join(name.split())
    
    # Remove trailing periods from abbreviations
    if name.endswith('.') and len(name) <= 3:
        name = name.rstrip('.')
    
    # Skip if too short or looks like an email
    if len(name) < 2 or '@' in name or name.lower() in ['to', 'from', 'cc', 'bcc']:
        return None
    
    # Skip if it's just numbers or special chars
    if not re.search(r'[a-zA-Z]', name):
        return None
    
    # Skip if it's mostly numbers (like "1.11M1")
    if len(re.sub(r'[^0-9]', '', name)) > len(name) * 0.5:
        return None
    
    # Skip if it has too many numbers or weird patterns
    if re.search(r'\d{3,}', name):  # Skip if has 3+ consecutive digits
        return None
    
    # Skip single letters or initials without context
    if len(name) <= 2 and name.isupper():
        return None
    
    # Skip if it's just punctuation or weird chars
    if re.match(r'^[\.\-\s_]+$', name):
        return None
    
    return name

def extract_names_from_file(filepath, filename):
    """Extract names from To: lines in a file."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if line.startswith('To:'):
                    # Get everything after "To:"
                    to_content = line[3:].strip()
                    
                    # Split on semicolons and commas
                    # First split on semicolons, then on commas
                    parts = []
                    for semicolon_part in to_content.split(';'):
                        for comma_part in semicolon_part.split(','):
                            parts.append(comma_part.strip())
                    
                    # Process each part
                    for part in parts:
                        if not part:
                            continue
                        
                        cleaned = clean_name(part)
                        if cleaned:
                            name_to_files[cleaned].add(filename)
                            name_counts[cleaned] += 1
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def main():
    # Process all email files recursively, but skip byDate subdirectories
    email_files = []
    for root, dirs, files in os.walk(email_dir):
        # Skip byDate directories to avoid duplicates
        if 'byDate' in root:
            continue
        for f in files:
            if f.endswith('.txt'):
                filepath = os.path.join(root, f)
                email_files.append((filepath, f))
    
    total_files = len(email_files)
    print(f"Processing {total_files} email files...")
    
    for filepath, filename in email_files:
        extract_names_from_file(filepath, filename)
    
    print(f"\nFound {len(name_to_files)} unique names")
    
    # Create files for each name, sorted by frequency
    for name, count in sorted(name_counts.items(), key=lambda x: x[1], reverse=True):
        # Create safe filename (prepend count, remove problematic chars)
        safe_name = re.sub(r'[^\w\s\-\.]', '', name)
        safe_name = safe_name.replace(' ', '_')
        safe_name = safe_name.replace('/', '_')
        safe_name = safe_name.replace('\\', '_')
        
        # Prepend count for sorting
        filename = f"({count}) {safe_name}"
        filepath = os.path.join(output_dir, filename)
        
        # Write list of files containing this name
        with open(filepath, 'w') as f:
            for email_file in sorted(name_to_files[name]):
                f.write(f"{email_file}\n")
    
    print(f"\nCreated {len(name_to_files)} name files in {output_dir}/")
    print(f"\nTop 20 names by frequency:")
    for name, count in sorted(name_counts.items(), key=lambda x: x[1], reverse=True)[:20]:
        print(f"  {name}: {count} occurrences in {len(name_to_files[name])} files")

if __name__ == '__main__':
    main()

