# Email Structure Analysis

## Standard Email Headers (Sortable Features)

### 1. **Date/Sent** ⭐ PRIMARY SORT FIELD
- **Format 1 (most common):** `Sent: 3/18/2016 4:30:13 PM`
- **Format 2:** `Sent: Friday, March 18, 2016 11:41 AM`
- **Format 3:** `Date: Fri, Mar 18, 2016 at 11:39 AM`
- **Format 4:** `Date: April 27, 2016 at 3:47:49 PM EDT`
- **Extraction:** Parse date from `^Sent:` or `^Date:` line
- **Sortable:** Yes - chronological sorting

### 2. **From (Sender)**
- **Format:** `From: jeffrey E. [jeeyacation@gmail.com]`
- **Variations:**
  - `From: Martin G. Weinberg`
  - `From: ` (empty/redacted)
  - `From: jeffrey E. [jeeyacation@gmail.com]`
- **Extraction:** Parse from `^From:` line
- **Sortable:** Yes - alphabetical by name or email

### 3. **To (Recipient)**
- **Format:** `To: Lisa New` or `To: jeevacation@gmail.com`
- **Variations:**
  - Multiple recipients: `To: 'effre E. 'eeyacation@gmail.com]; Kathy Ruemmler; Darren Indyke`
  - Empty/redacted: `To: `
- **Extraction:** Parse from `^To:` line
- **Sortable:** Yes - alphabetical

### 4. **Subject**
- **Format:** `Subject: Re: Thank You from Lisa and Poetry in America`
- **Variations:**
  - `Subject: Fwd: Patterson`
  - `Subject: ATTORNEY-CLIENT PRIVILEGE`
- **Extraction:** Parse from `^Subject:` line
- **Sortable:** Yes - alphabetical

### 5. **Importance** (Optional)
- **Format:** `Importance: High`
- **Values:** `High`, `Normal` (or absent)
- **Extraction:** Parse from `^Importance:` line
- **Sortable:** Yes - High first, then Normal, then None

### 6. **Cc/Bcc** (Optional)
- **Format:** `Cc: Scott Stalfilh<...>; JR Stambaugh <...>`
- **Extraction:** Parse from `^Cc:` or `^Bcc:` line
- **Sortable:** Yes - count of recipients or alphabetical

## Content-Based Features (Sortable)

### 7. **Is Forwarded Email**
- **Indicators:**
  - `----------Forwarded message`
  - `-----Original Message-----`
  - `Subject: Fwd: ...`
- **Extraction:** Search for forward indicators
- **Sortable:** Yes - boolean (forwarded vs. original)

### 8. **Has Attachments**
- **Indicators:**
  - `Content-Disposition: ATTACHMENT;`
  - `filename=photo_1.3PG`
  - `Content-Transfer-Encoding: BASE64`
- **Extraction:** Search for attachment indicators
- **Sortable:** Yes - boolean (has attachments vs. no attachments)

### 9. **Has Legal Disclaimer**
- **Indicators:**
  - `attorney-client privileged`
  - `Privileged - Redacted`
  - `confidential, may be attorney-client privileged`
  - `copyright -all rights reserved`
- **Extraction:** Search for legal disclaimer keywords
- **Sortable:** Yes - boolean (has disclaimer vs. no disclaimer)

### 10. **Email Domain**
- **Extraction:** Extract domain from From/To email addresses
- **Examples:** `gmail.com`, `harvard.edu`, etc.
- **Sortable:** Yes - alphabetical by domain

### 11. **Is Reply**
- **Indicators:**
  - `Subject: Re: ...`
  - `On [date], [person] wrote:`
- **Extraction:** Check subject line or body for reply indicators
- **Sortable:** Yes - boolean (reply vs. original)

## Metadata Features

### 12. **Document ID**
- **Format:** `HOUSE OVERSIGHT 019330` (appears at end of file)
- **Extraction:** Extract number from filename or end of file
- **Sortable:** Yes - numerical

### 13. **Email Length**
- **Extraction:** Count lines or characters in email body
- **Sortable:** Yes - numerical

### 14. **Has Multiple Recipients**
- **Extraction:** Count recipients in To/Cc/Bcc fields
- **Sortable:** Yes - numerical

## Recommended Sorting Priorities

1. **Date/Sent** - Most useful for chronological analysis
2. **From** - Group by sender
3. **Subject** - Group related conversations
4. **To** - Group by recipient
5. **Has Attachments** - Separate emails with attachments
6. **Is Forwarded** - Separate forwarded vs. original emails
7. **Importance** - High priority emails first

## Example Email Structure

```
From: jeffrey E. [jeeyacation@gmail.com]
Sent: 12/19/2016 3:01:54 PM
To: Lisa New
Subject: Re: Thank You from Lisa and Poetry in America
[email body]
HOUSE OVERSIGHT 019330
```

## Parsing Recommendations

1. Use regex patterns to extract header fields
2. Normalize date formats to ISO 8601 for consistent sorting
3. Handle redacted/empty fields gracefully
4. Extract email addresses from brackets `[email@domain.com]`
5. Detect forwarded emails by checking for forward indicators
6. Count attachments by searching for `Content-Disposition: ATTACHMENT`

