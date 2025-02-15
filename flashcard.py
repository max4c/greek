import pdfplumber
import re
import os

def extract_word_pairs(pdf_path, output_path):
    # Open the PDF
    with pdfplumber.open(pdf_path) as pdf:
        all_text = ''
        for page in pdf.pages:
            all_text += page.extract_text() + '\n'
    
    # Split into lines and process
    lines = all_text.split('\n')
    word_pairs = []
    
    for line in lines:
        # Skip header lines and empty lines
        if not line.strip() or any(header in line.upper() for header in 
            ['WORD CLASS', 'UNIT', 'PAGE', 'PAGES', '-', 'THE FOLLOWING']):
            continue
            
        # Match pattern: english_word (pos) greek_word
        match = re.match(r'^(.*?)\s*\([^)]+\)\s+(\S+)', line.strip())
        if match:
            eng = match.group(1).strip()
            greek = match.group(2).strip()
            
            # Clean up the words
            eng = re.sub(r'\s+', ' ', eng).strip()
            greek = greek.split(',')[0].strip()  # Take first translation if multiple
            
            # Skip if either part is empty or contains only numbers/punctuation
            if eng and greek and not re.match(r'^[\d\–\-\s]+$', eng) and not re.match(r'^[\d\–\-\s]+$', greek):
                word_pairs.append(f"{eng} <> {greek}")
    
    # Write to output file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(word_pairs))

def process_pdfs():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    for filename in os.listdir(current_dir):
        if filename.endswith('_Wordlist_GR.pdf'):
            pdf_path = os.path.join(current_dir, filename)
            output_path = os.path.join(current_dir, filename.replace('.pdf', '.txt'))
            extract_word_pairs(pdf_path, output_path)
            print(f"Processed {filename} -> {filename.replace('.pdf', '.txt')}")

if __name__ == "__main__":
    process_pdfs()