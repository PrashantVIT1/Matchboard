"""Text cleaning utilities for resume text extraction."""

import re


def clean_extracted_text(text: str) -> str:
    """
    Clean extracted text from PDF.
    
    Removes excessive whitespace, repeated blank lines, and other artifacts
    while preserving the original information.
    
    Args:
        text: Raw extracted text
    
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    # Replace multiple spaces with single space
    text = re.sub(r' +', ' ', text)
    
    # Replace multiple newlines with double newline (preserve paragraph breaks)
    text = re.sub(r'\n\n+', '\n\n', text)
    
    # Replace single newlines with space (join lines that should be together)
    # But be careful not to join actual paragraph breaks
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
    
    # Remove excessive whitespace again after line joining
    text = re.sub(r' +', ' ', text)
    
    # Remove leading/trailing whitespace again
    text = text.strip()
    
    return text
