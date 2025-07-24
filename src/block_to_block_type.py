from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    """
    Determine the type of a markdown block.
    
    Takes a single block of markdown text and returns the BlockType
    representing what type of block it is.
    
    Args:
        block (str): A single block of markdown text (whitespace already stripped)
        
    Returns:
        BlockType: The type of the block
        
    Block type rules:
    - Headings: Start with 1-6 # characters, followed by a space
    - Code blocks: Must start and end with 3 backticks
    - Quote blocks: Every line must start with >
    - Unordered lists: Every line must start with - followed by space
    - Ordered lists: Every line must start with number. followed by space, incrementing from 1
    - Paragraph: If none of the above conditions are met
    """
    lines = block.split('\n')
    
    # Check for heading (1-6 # followed by space, single line only)
    if len(lines) == 1 and re.match(r'^#{1,6} ', block):
        return BlockType.HEADING
    
    # Check for code block (starts and ends with ```)
    if block.startswith('```') and block.endswith('```') and len(block) > 6:
        return BlockType.CODE
    
    # Check for quote block (every line starts with >)
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    
    # Check for unordered list (every line starts with "- ")
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST
    
    # Check for ordered list (every line starts with number. followed by space, incrementing from 1)
    if _is_ordered_list(lines):
        return BlockType.ORDERED_LIST
    
    # Default to paragraph
    return BlockType.PARAGRAPH

def _is_ordered_list(lines):
    """
    Helper function to check if lines form a valid ordered list.
    
    Args:
        lines (list): List of lines to check
        
    Returns:
        bool: True if lines form a valid ordered list, False otherwise
    """
    for i, line in enumerate(lines):
        expected_number = i + 1
        expected_start = f"{expected_number}. "
        
        if not line.startswith(expected_start):
            return False
    
    return True
