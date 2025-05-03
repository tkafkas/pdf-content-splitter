import os
from PyPDF2 import PdfReader, PdfWriter
import re

def extract_account_number(text):
    """Extract the account number that follows ΛΟΓΑΡΙΑΣΜΟΣ"""
    # Try different possible encodings of the Greek word
    patterns = [
        r'ΛΟΓΑΡΙΑΣΜΟΣ\s*:?\s*([^\n\r]+)',
        r'ΛΟΓΑΡΙΑΣΜΟΣ\s*:?\s*([^\n\r]+)',
        r'ΛΟΓΑΡΙΑΣΜΟΣ\s*:?\s*([^\n\r]+)',
        r'ΛΟΓΑΡΙΑΣΜ[ΟΌ]Σ\s*:?\s*([^\n\r]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.UNICODE)
        if match:
            account = match.group(1).strip()
            # Remove spaces, dashes, and clean the account number for filename use
            account = re.sub(r'[\s-]+', '', account)
            account = re.sub(r'[<>:"/\\|?*]', '_', account)
            # Remove any dots and underscores
            account = re.sub(r'[._]+', '', account)
            return account
    return None

def split_pdf_by_content(input_path, output_dir=None, split_text=None):
    """
    Split a PDF file into multiple PDFs based on content
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"PDF file not found: {input_path}")
    
    # Set output directory
    if output_dir is None:
        output_dir = os.path.dirname(input_path) or "."
    os.makedirs(output_dir, exist_ok=True)
    
    # Create PDF reader object
    reader = PdfReader(input_path)
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    
    # Store sections
    sections = []
    current_pdf = PdfWriter()
    current_text = ""
    
    print(f"Total pages in PDF: {len(reader.pages)}")
    
    # First page is always a start of a section
    sections.append({"start": 0, "text": ""})
    
    # Find all section starts
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        print(f"Page {i+1} content preview: {text[:100]}...")
        
        # Check for account number on this page
        if i > 0 and extract_account_number(text):  # Skip first page check as it's already a section
            print(f"Found new account on page {i+1}")
            sections.append({"start": i, "text": ""})
    
    print(f"Found {len(sections)} sections")
    
    # Process sections
    for i, section in enumerate(sections):
        start_page = section["start"]
        end_page = sections[i+1]["start"] if i+1 < len(sections) else len(reader.pages)
        
        # Create PDF for this section
        output = PdfWriter()
        section_text = ""
        
        # Add pages to this section
        for page_num in range(start_page, end_page):
            page = reader.pages[page_num]
            output.add_page(page)
            section_text += page.extract_text()
        
        # Get account number and save
        account_number = extract_account_number(section_text)
        if account_number:
            output_path = os.path.join(output_dir, f"{base_name}_{account_number}.pdf")
            with open(output_path, "wb") as output_file:
                output.write(output_file)
            print(f"Created: {output_path} (pages {start_page + 1}-{end_page})")
        else:
            print(f"Warning: Could not extract account number for section {i+1} (pages {start_page + 1}-{end_page})")
            print(f"Section text preview: {section_text[:200]}...")

def main():
    """Main function to run the PDF splitter"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Split PDF based on content")
    parser.add_argument("input_pdf", help="Path to the input PDF file")
    parser.add_argument("-o", "--output-dir", help="Output directory for split PDFs")
    parser.add_argument("-s", "--split-text", help="Text to use as split point")
    
    args = parser.parse_args()
    
    try:
        split_pdf_by_content(args.input_pdf, args.output_dir, args.split_text)
        print("PDF splitting completed successfully!")
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())