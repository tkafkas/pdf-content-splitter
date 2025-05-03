# PDF Content Splitter

A Python-based utility that intelligently splits PDF documents into multiple files based on text content. The tool searches for specific text patterns within the PDF and creates separate documents at each occurrence, making it ideal for breaking down large PDFs into smaller, logically separated files.

## Features

- Simple drag-and-drop interface
- Customizable split text markers
- Intelligent text pattern detection
- Preserves original PDF quality
- Organized output directory structure
- Support for various text encodings
- Both GUI and command-line interfaces

## Requirements

- Python 3.x
- PyPDF2 >= 3.0.0
- Windows OS

## Installation

1. Ensure Python 3.x is installed on your system
2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Simple Method (Recommended)
1. Drag and drop your PDF file onto `split_pdf.bat`
2. The tool will create a new folder named `[OriginalFileName]Split` containing the individual PDFs
3. Each split PDF will be named using the format: `[OriginalFileName]_[Identifier].pdf`

### Command Line Usage

The script can be run directly using Python with custom parameters:

```bash
python pdf_splitter.py input.pdf [-o output_directory] [-s split_text]
```

Parameters:
- `input.pdf`: Path to the PDF file to split
- `-o, --output-dir`: Optional output directory (default: creates 'Split' folder next to input file)
- `-s, --split-text`: Optional text pattern to use as split point

## How It Works

1. The tool scans each page of the PDF for the specified text pattern
2. When found, it extracts relevant identifier information
3. Creates a new PDF starting from that page until the next marker or end of document
4. Saves each section as a separate PDF with appropriate naming
5. Handles various text patterns and encodings for reliable extraction

## Output

- Creates a new directory named `[OriginalFileName]Split`
- Generates separate PDFs for each section
- Files are named using the pattern: `[OriginalFileName]_[Identifier].pdf`
- Maintains original PDF quality and formatting

## Example

If you have a PDF named `Document_20240131.pdf` containing multiple sections:

```
Original:
└── Document_20240131.pdf

After splitting:
└── Document_20240131Split/
    ├── Document_20240131_001.pdf
    ├── Document_20240131_002.pdf
    └── Document_20240131_003.pdf
```

## Notes

- The tool can be configured to split on any text pattern
- Section identifiers are cleaned of spaces and special characters
- If an identifier cannot be extracted, the section will be logged but not saved
- For best results, ensure PDF text is properly encoded and extractable
- Processing time depends on PDF size and complexity