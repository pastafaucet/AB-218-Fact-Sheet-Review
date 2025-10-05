import pdfplumber
import pandas as pd
import re
from pathlib import Path

def assess_completeness(text):
    """Assess how complete the fact sheet is based on filled fields"""
    # Check education section completeness
    education_markers = [
        'Grammar School(s):',
        'Middle School or Junior High School:',
        'High School:',
        'College:'
    ]
    
    # Check employment section
    employment_filled = 'NOT EMPLOYED' not in text
    
    # Count filled education sections
    filled_education = 0
    for marker in education_markers:
        if marker in text:
            # Check if there's actual content after the marker
            pattern = rf'{re.escape(marker)}.*?Name:\s*(\S+)'
            match = re.search(pattern, text, re.DOTALL)
            if match and match.group(1).strip():
                filled_education += 1
    
    # Determine completeness level
    if filled_education >= 3 and employment_filled:
        return "Fully Complete"
    elif filled_education >= 2:
        return "Mostly Complete"
    elif filled_education >= 1:
        return "Somewhat Complete"
    else:
        return "Sparse"

def extract_plaintiff_name(text):
    """Extract plaintiff's full name"""
    pattern = r'Full Name of\s+Plaintiff:\s*(.+?)(?:\n|Other names)'
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return ""

def extract_perpetrator_details(text):
    """Extract verbatim perpetrator details from the three questions"""
    details = []
    
    # Question 1: Identity the accused perpetrator(s)
    pattern1 = r'1\.\s+Identity the accused perpetrator\(s\).*?:\s*(.+?)(?=\n\s*2\.|\Z)'
    match1 = re.search(pattern1, text, re.DOTALL | re.IGNORECASE)
    if match1:
        identity = match1.group(1).strip()
        details.append(identity)
    
    # Question 2: Description of abuser
    pattern2 = r'2\.\s+If you are unable to identify.*?:\s*(.+?)(?=\n\s*3\.|\Z)'
    match2 = re.search(pattern2, text, re.DOTALL | re.IGNORECASE)
    if match2:
        description = match2.group(1).strip()
        if description and description != "":
            details.append(description)
    
    # Question 3: Relationship with County
    pattern3 = r'3\.\s+Specify the accused perpetrator.*?:\s*(.+?)(?=\n\s*Relationship to Accused|\Z)'
    match3 = re.search(pattern3, text, re.DOTALL | re.IGNORECASE)
    if match3:
        relationship = match3.group(1).strip()
        details.append(relationship)
    
    return "\n\n".join(details)

def extract_abuse_details(text):
    """Extract verbatim abuse details - the entire 'Description and Report of Sex Abuse' section"""
    # Find the section starting from "Description and Report of Sex Abuse" 
    # through "Knowledge and complaints"
    start_pattern = r'Description and Report of Sex Abuse\.'
    end_pattern = r'Knowledge and complaints'
    
    start_match = re.search(start_pattern, text, re.IGNORECASE)
    end_match = re.search(end_pattern, text, re.IGNORECASE)
    
    if start_match and end_match:
        # Extract everything between these two markers
        abuse_section = text[start_match.end():end_match.start()].strip()
        return abuse_section
    
    return ""

def extract_factsheet_data(pdf_path):
    """Extract all required data from a single PDF factsheet"""
    with pdfplumber.open(pdf_path) as pdf:
        # Extract text from all pages
        full_text = ""
        for page in pdf.pages:
            full_text += page.extract_text() + "\n"
    
    # Extract each column's data
    plaintiff_name = extract_plaintiff_name(full_text)
    completeness = assess_completeness(full_text)
    perpetrator_details = extract_perpetrator_details(full_text)
    abuse_details = extract_abuse_details(full_text)
    
    return {
        'Plaintiff Full Name': plaintiff_name,
        'Completeness': completeness,
        'Perpetrator Details': perpetrator_details,
        'Abuse Details': abuse_details
    }

def main():
    # Test with Rodriguez file
    pdf_path = "DTLA Law Fact Sheets/[23CHCV01842] [Rodriguez, Jesse] [John Doe JR] [0560-001-JR].pdf"
    
    print(f"Processing: {pdf_path}")
    data = extract_factsheet_data(pdf_path)
    
    # Create DataFrame
    df = pd.DataFrame([data])
    
    # Save to Excel
    output_file = "factsheet_test_output.xlsx"
    df.to_excel(output_file, index=False, engine='openpyxl')
    
    print(f"\n✓ Excel file created: {output_file}")
    print(f"\nExtracted Data Preview:")
    print(f"Plaintiff: {data['Plaintiff Full Name']}")
    print(f"Completeness: {data['Completeness']}")
    print(f"\nPerpetrator Details:\n{data['Perpetrator Details'][:200]}...")
    print(f"\nAbuse Details:\n{data['Abuse Details'][:200]}...")

if __name__ == "__main__":
    main()
