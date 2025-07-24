from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Split TextNodes based on delimiter patterns.
    
    Takes a list of TextNodes and splits any TEXT type nodes that contain
    the specified delimiter into multiple nodes with appropriate text types.
    
    Args:
        old_nodes (list): List of TextNode objects to process
        delimiter (str): The delimiter to split on (e.g., "**", "*", "`")
        text_type (TextType): The TextType to assign to text between delimiters
        
    Returns:
        list: New list of TextNode objects with split nodes
        
    Raises:
        ValueError: If delimiter pairs are unmatched (odd number of delimiters)
    """
    new_nodes = []
    
    for node in old_nodes:
        # Only process TEXT type nodes, pass others through unchanged
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
            
        # Split the text by the delimiter
        parts = node.text.split(delimiter)
        
        # If there's only one part, no delimiter was found
        if len(parts) == 1:
            new_nodes.append(node)
            continue
            
        # Check for unmatched delimiters (must have even number of parts after split)
        # Because split on delimiter creates: text|delimiter|text|delimiter|text
        # So we need odd number of parts for even number of delimiters
        if len(parts) % 2 == 0:
            raise ValueError(f"Unmatched delimiter '{delimiter}' in text: {node.text}")
        
        # Process the parts alternately as TEXT and the specified text_type
        for i, part in enumerate(parts):
            # Skip empty parts
            if part == "":
                continue
                
            if i % 2 == 0:
                # Even indices are regular text (outside delimiters)
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                # Odd indices are inside delimiters (should be converted)
                new_nodes.append(TextNode(part, text_type))
    
    return new_nodes
