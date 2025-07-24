def markdown_to_blocks(markdown):
    """
    Split markdown text into blocks based on blank lines.
    
    Takes a raw markdown string representing a full document and returns
    a list of block strings. Blocks are separated by blank lines (double newlines).
    
    Args:
        markdown (str): Raw markdown text to split into blocks
        
    Returns:
        list: List of block strings, with leading/trailing whitespace stripped
               and empty blocks removed
    
    Example:
        markdown = "# Heading\n\nParagraph text\n\n- List item"
        blocks = markdown_to_blocks(markdown)
        # Returns: ["# Heading", "Paragraph text", "- List item"]
    """
    # Split on double newlines to separate blocks
    raw_blocks = markdown.split('\n\n')
    
    # Process each block: strip whitespace and filter out empty blocks
    blocks = []
    for block in raw_blocks:
        # Strip leading and trailing whitespace from the block
        stripped_block = block.strip()
        
        # Only add non-empty blocks
        if stripped_block:
            blocks.append(stripped_block)
    
    return blocks
