# House Oversight Committee Documents - Data Mining Repository

This repository contains House Oversight Committee documents related to Jeffrey Epstein, organized and analyzed for data mining purposes.

## Repository Structure

### `/input/`
**Original source files (2,895 total documents)**

- `TEXT.zip` - Original compressed archive
- `TEXT.zip emails/` - 2,271 email files (extracted and sorted)
- `TEXT.zip non-emails/` - 624 non-email documents

### `/output/`
**Processed and organized email files**

- `email/` - All email files organized by various criteria
  - `byDate/` - Emails organized chronologically by year/month/day
    - Structure: `YYYY/MM/DD/HOUSE_OVERSIGHT_XXXXXX.txt`
    - Date range: 2006-2019
    - All 2,271 emails successfully dated and organized
  - `importanceHigh/` - 1,480 emails marked with "Importance: High" flag
    - Represents 65.1% of all emails

### `/analysis/`
**Extracted data and analysis results**

#### Email Analysis
- `emails/byFreq.txt` - 691 unique email addresses sorted by frequency
  - Format: `email (count)`
  - Top emails: jeevacation@gmail.com (6,564), jeeitunes@gmail.com (2,633)
  
- `emails/byDomain/` - 261 domain files
  - Format: `(count) domain` (no extension, count prepended for sorting)
  - Each file contains all email addresses for that domain
  - Top domains: baml.com (99), gmail.com (49), ubs.com (45)
  
- `emails.txt` - Complete list of all 691 unique email addresses (alphabetical)

#### Name Analysis
- `names/byFreq/` - 582 unique names extracted from "To:" fields
  - Format: `(count) Name` (no extension, count prepended)
  - Each file contains list of email filenames where that name appears
  - Names split on semicolons and commas
  - Top names: jeffrey E (659), Jeffrey Epstein (406), Weingarten (332)

## File Naming Convention

All documents follow the pattern: `HOUSE_OVERSIGHT_XXXXXX.txt`

Where `XXXXXX` is a 6-digit document identifier.

## Email File Structure

Email files contain standard email headers:
- `From:` - Sender name/email
- `Sent:` or `Date:` - Date/time (various formats)
- `To:` - Recipient(s), may contain multiple names/emails separated by semicolons or commas
- `Subject:` - Email subject line
- `Importance:` - Optional priority flag (High/Normal)

## Statistics

- **Total documents:** 2,895
- **Email files:** 2,271 (78.4%)
- **Non-email files:** 624 (21.6%)
- **Emails with dates:** 2,271 (100%)
- **High importance emails:** 1,480 (65.1%)
- **Unique email addresses:** 691
- **Unique domains:** 261
- **Unique names:** 582

## Date Distribution

- **2006-2008:** 18 files
- **2009-2014:** 413 files
- **2015-2019:** 1,840 files (peak activity)
  - 2016: 494 files
  - 2017: 499 files
  - 2018: 463 files

## Usage

### Finding emails by date
```bash
# All emails from a specific date
ls output/email/byDate/2016/11/10/

# All emails from a year
find output/email/byDate/2016 -name "*.txt"
```

### Finding emails by domain
```bash
# All emails from a specific domain
cat "analysis/emails/byDomain/(49) gmail.com"
```

### Finding emails by name
```bash
# All emails sent to a specific person
cat "analysis/names/byFreq/(659) jeffrey_E"
```

### Finding high importance emails
```bash
# All high importance emails
ls output/email/importanceHigh/
```

## Notes

- All email files have been successfully parsed for dates (100% coverage)
- Names are extracted from "To:" fields and cleaned of special characters
- Email addresses are normalized and organized by domain
- Files are organized to enable efficient searching and analysis

