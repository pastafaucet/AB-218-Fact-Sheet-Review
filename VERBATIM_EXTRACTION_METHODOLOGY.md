# Verbatim Factsheet Extraction Methodology

## Project Overview
This document explains the exact methodology used to extract verbatim text from DTLA factsheet PDFs and organize them into a structured Excel spreadsheet with consistent formatting.

## Goal
Extract detailed, verbatim information from legal factsheets (abuse allegations) into an Excel file with 7 columns, maintaining consistent concise formatting across all entries.

---

## Excel Structure

### Columns (7 total):
1. **Plaintiff Full Name**
2. **Completeness**
3. **Perpetrator Details**
4. **Summary of Abuse**
5. **Abuse Details**
6. **Mental Health Treatment**
7. **Credibility Notes**

### Column Widths:
```python
ws.column_dimensions['A'].width = 25  # Plaintiff Full Name
ws.column_dimensions['B'].width = 35  # Completeness
ws.column_dimensions['C'].width = 50  # Perpetrator Details
ws.column_dimensions['D'].width = 30  # Summary of Abuse
ws.column_dimensions['E'].width = 80  # Abuse Details
ws.column_dimensions['F'].width = 35  # Mental Health Treatment
ws.column_dimensions['G'].width = 50  # Credibility Notes
```

---

## Column Format Guidelines

### 1. Plaintiff Full Name
- Simple text: First Last (no quotes)
- If supplemental filing: `First Last (First Supplemental)`

### 2. Completeness
**CRITICAL: Keep this CONCISE and scannable**

Format:
```
[Overall Rating] ([Percentage])

✅ [Category]: [Brief status]
❌ [Category]: [Brief status]
⚠️ [Category]: [Brief status]
```

**Example (GOOD - Concise):**
```
Mostly Complete (75%)

✅ Personal Information: Complete
✅ Education: 12th grade, Job Core
❌ Employment: NONE in last 5 years
✅ Probation: 2006-2009
⚠️ Perpetrator ID: Description but unnamed
✅ Abuse Details: Detailed
✅ Complaints: Told Rachel - dismissed, retaliation
✅ Damages: Complete
✅ Mental Health: Dr. Khodaparest
```

**Categories to include:**
- Personal Information
- Education/Education History
- Employment/Employment History
- Probation/Probation History
- Perpetrator ID/Perpetrator Identification
- Abuse Details
- Complaints/Knowledge/Complaints
- Damages/Damages/Injuries
- Mental Health/Medical Treatment

**Status indicators:**
- ✅ = Complete/Present
- ❌ = None/Missing
- ⚠️ = Partial/Concerning

### 3. Perpetrator Details
Format by facility:

```
[FACILITY NAME] ([Years], Age [X])
Number: [X] perpetrator(s)

[For each perpetrator:]
Name: [Name if known] OR Perp 1/P1/Perpetrator 1
Description: [Physical description]
Position: [Role at facility]
```

**Example:**
```
CAMP MCNAIR (2006-2009, Age 13-16)
Number: 1 perpetrator
Description: Male, Caucasian, 30's, receding hairline, 5'7, heavyset (beer gut), distinctive scar on left arm (4-5 inches, keloid)
Position: Staff Member
```

### 4. Summary of Abuse
Brief comma-separated list of abuse types:

```
[Type 1], [Type 2], [Type 3]
```

**Example:**
```
Groping, attempted digital penetration, voyeurism (masturbating during strip search)
```

If concerns exist, prefix with ⚠️:
```
⚠️ Pepper spray to genitals, physical abuse
```

### 5. Abuse Details
**Most detailed section - verbatim text from factsheet**

Format:
```
**[FACILITY NAME] (Age [X], [Year]):**

[Detailed description of incidents, verbatim from factsheet]

Location: [Where abuse occurred]

[If complaint made:]
COMPLAINT MADE: [Details]
```

**Example:**
```
**CAMP MCNAIR (Age 13-16, 2006-2009):**

Guard came to cell to "check if she was alive." Helped her undress, said "You're moving to slow." Fondled breasts. When she turned and bent over, attempted digital penetration - she kicked him.

Another incident: noticed him masturbating during strip search.

Would take phone calls away if she refused.

Location: Intake

COMPLAINT MADE: Told Staff Member Rachel who said client was "exaggerating." When she kept reporting, perpetrator was assigned to her MORE. Eventually moved to different unit.
```

### 6. Mental Health Treatment
Standard format for Dr. Khodaparest (primary provider):

```
Dr. Neda Khodaparest, PsyD
The Green Room Psychological Services
5252 Balboa Ave., Suite 502, San Diego, CA 92117
858-480-9118
Treatment: Therapy for PTSD and other diagnoses
```

If additional providers, add below with blank line separator.

### 7. Credibility Notes
**CRITICAL: Keep this BRIEF and scannable**

Format:
```
[Concern Level] - [Key issue in 5-10 words]

**Strengths:** [Brief bullet points]
**Concerns:** [Brief bullet points]

Overall: [One sentence conclusion]
```

**Concern Levels:**
- `No credibility concerns identified.`
- `Minor concerns -`
- `Moderate concerns -`
- `⚠️ SIGNIFICANT CONCERNS -`
- `⚠️⚠️ SEVERE CREDIBILITY CONCERNS -`

**Example (GOOD - Concise):**
```
Moderate concerns - Reported with retaliation.

**Strengths:** Distinctive scar, direct quote, reported to Rachel, retaliation (assigned MORE), kicked him.
**Concerns:** Perpetrator unnamed, no employment.

Overall: Credible. Failed reporting with retaliation supports account.
```

**Example (BAD - Too verbose):**
```
Moderate credibility concerns: Female victim reported to staff member Rachel who dismissed the claim as the plaintiff "exaggerating." When the plaintiff continued to report the abuse, the perpetrator was actually assigned to her MORE frequently as a form of retaliation, which demonstrates a pattern of institutional failure to protect victims...
[continues for several paragraphs]
```

---

## Python Script Template

### Full Working Script:
```python
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Alignment

# Read existing Excel file (if adding to existing)
existing_df = pd.read_excel('Enhanced_First_20_Files_VERBATIM_COMPLETE.xlsx')

# Create new entries
new_entries = [
    {
        'Plaintiff Full Name': 'Name Here',
        'Completeness': '''Rating (%)

✅ Category: Status
❌ Category: Status
''',
        'Perpetrator Details': '''FACILITY (Year, Age X)
Number: X
Description: Details
Position: Role''',
        'Summary of Abuse': 'Type 1, Type 2',
        'Abuse Details': '''**FACILITY (Age X, Year):**

Details here

Location: Location''',
        'Mental Health Treatment': '''Dr. Neda Khodaparest, PsyD
The Green Room Psychological Services
5252 Balboa Ave., Suite 502, San Diego, CA 92117
858-480-9118
Treatment: Therapy for PTSD and other diagnoses''',
        'Credibility Notes': '''Level - Summary

**Strengths:** Points
**Concerns:** Points

Overall: Conclusion.'''
    }
    # Add more entries...
]

# Create DataFrame
new_df = pd.DataFrame(new_entries)

# Combine with existing (or use new_df alone)
all_df = pd.concat([existing_df, new_df], ignore_index=True)

# Save to Excel
output_file = 'Output_File_Name.xlsx'
all_df.to_excel(output_file, index=False, engine='openpyxl')

# Format the Excel file
wb = load_workbook(output_file)
ws = wb.active

# Set column widths
ws.column_dimensions['A'].width = 25
ws.column_dimensions['B'].width = 35
ws.column_dimensions['C'].width = 50
ws.column_dimensions['D'].width = 30
ws.column_dimensions['E'].width = 80
ws.column_dimensions['F'].width = 35
ws.column_dimensions['G'].width = 50

# Enable text wrapping for all cells
for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=7):
    for cell in row:
        cell.alignment = Alignment(wrap_text=True, vertical='top')

wb.save(output_file)

print(f"✅ Successfully created {output_file}")
print(f"   Total entries: {len(all_df)}")
```

---

## Key Principles

### 1. CONSISTENCY IS CRITICAL
- All 30 files must use IDENTICAL formatting
- If files 1-20 are concise, files 21-30 MUST match that exact level of conciseness
- Do NOT make later files more verbose than earlier files

### 2. BREVITY IN ANALYSIS SECTIONS
- **Completeness**: Bullet points, NO paragraphs
- **Credibility Notes**: 3-5 lines maximum
  - One line: Concern level + key issue
  - One line: Strengths (brief)
  - One line: Concerns (brief)
  - One line: Overall conclusion

### 3. DETAIL IN FACTS SECTIONS
- **Abuse Details**: Full verbatim text from factsheet
- Include direct quotes
- Preserve specific details (ages, dates, locations)

### 4. FORMATTING CONSISTENCY
- Use ✅ ❌ ⚠️ symbols consistently
- Always include blank lines between sections
- Triple backticks for code blocks
- Use **bold** for facility names in Abuse Details

---

## Common Mistakes to Avoid

### ❌ WRONG: Verbose Completeness
```
✅ Personal Information: Complete with full details provided including mother's name, father's name, dates of birth for all family members, current residence address, and comprehensive family background information that supports the overall credibility of the factsheet.
```

### ✅ RIGHT: Concise Completeness
```
✅ Personal Information: Complete
```

---

### ❌ WRONG: Verbose Credibility Notes
```
Moderate credibility concerns have been identified in this case. The primary strength of this account is that the plaintiff provided a detailed physical description of the perpetrator including a distinctive scar on the left arm measuring 4-5 inches which would be identifiable. Additionally, the plaintiff reported the abuse to Staff Member Rachel, and when Rachel dismissed the complaint as "exaggerating," the plaintiff continued to report, which demonstrates consistency in the account. As retaliation, the perpetrator was actually assigned to the plaintiff MORE frequently after the complaints were made, which is documented and supports the account. The plaintiff also took defensive action by kicking the perpetrator during one assault attempt. However, there are some concerns including the fact that the perpetrator was never named in the factsheet, and the plaintiff has had no employment in the last 5 years which may affect credibility perception. Overall, despite these concerns, the account is considered credible primarily because the failed reporting with documented retaliation supports the overall narrative and provides corroboration.
```

### ✅ RIGHT: Concise Credibility Notes
```
Moderate concerns - Reported with retaliation.

**Strengths:** Distinctive scar, direct quote, reported to Rachel, retaliation (assigned MORE), kicked him.
**Concerns:** Perpetrator unnamed, no employment.

Overall: Credible. Failed reporting with retaliation supports account.
```

---

## Process for New Files

### Step 1: Read the Factsheet PDF
Extract all verbatim text from the PDF

### Step 2: Organize Information
Map factsheet sections to Excel columns:
- Personal info → Completeness section
- Perpetrator description → Perpetrator Details
- Abuse allegations → Abuse Details (verbatim)
- Mental health providers → Mental Health Treatment
- Overall assessment → Credibility Notes

### Step 3: Apply Consistent Formatting
Use the exact format templates above for each column

### Step 4: Review for Consistency
Compare new entries to existing entries - they should look IDENTICAL in structure and length (except Abuse Details which varies by content)

### Step 5: Execute Python Script
Run the script to generate Excel file with proper formatting

---

## Quality Control Checklist

Before finalizing:
- [ ] Completeness section is bullet points, NOT paragraphs
- [ ] Credibility Notes is 3-5 lines MAXIMUM
- [ ] All ✅ ❌ ⚠️ symbols used consistently
- [ ] Column widths set correctly
- [ ] Text wrapping enabled
- [ ] Verbatim quotes included in Abuse Details
- [ ] Facility names bolded in Abuse Details
- [ ] Format matches existing entries EXACTLY

---

## Example Complete Entry

```python
{
    'Plaintiff Full Name': 'Teona Hunter',
    'Completeness': '''Mostly Complete (75%)

✅ Personal Information: Complete
✅ Education: 12th grade, Job Core
❌ Employment: NONE in last 5 years
✅ Probation: 2006-2009
⚠️ Perpetrator ID: Description but unnamed
✅ Abuse Details: Detailed
✅ Complaints: Told Rachel - dismissed, retaliation
✅ Damages: Complete
✅ Mental Health: Dr. Khodaparest''',
    
    'Perpetrator Details': '''CAMP MCNAIR (2006-2009, Age 13-16)
Number: 1 perpetrator
Description: Male, Caucasian, 30's, receding hairline, 5'7, heavyset (beer gut), distinctive scar on left arm (4-5 inches, keloid)
Position: Staff Member''',
    
    'Summary of Abuse': 'Groping, attempted digital penetration, voyeurism (masturbating during strip search)',
    
    'Abuse Details': '''CAMP MCNAIR (2006-2009, Age 13-16, 4-5x until moved to different unit)

Guard came to cell to "check if she was alive." Helped her undress, said "You're moving to slow." Fondled breasts. When she turned and bent over, attempted digital penetration - she kicked him.

Another incident: noticed him masturbating during strip search.

Would take phone calls away if she refused.

Location: Intake

COMPLAINT MADE: Told Staff Member Rachel who said client was "exaggerating." When she kept reporting, perpetrator was assigned to her MORE. Eventually moved to different unit.''',
    
    'Mental Health Treatment': '''Dr. Neda Khodaparest, PsyD
The Green Room Psychological Services
5252 Balboa Ave., Suite 502, San Diego, CA 92117
858-480-9118
Treatment: Therapy for PTSD and other diagnoses''',
    
    'Credibility Notes': '''Moderate concerns - Reported with retaliation.

**Strengths:** Distinctive scar, direct quote, reported to Rachel, retaliation (assigned MORE), kicked him.
**Concerns:** Perpetrator unnamed, no employment.

Overall: Credible. Failed reporting with retaliation supports account.'''
}
```

---

## Version History
- v1.0 (2025-10-05): Initial methodology document created after successful completion of 30-file extraction
