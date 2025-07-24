from textnode import TextNode, TextType
from extract_markdown import extract_markdown_images, extract_markdown_links

def split_nodes_image(old_nodes):
    """
    Split TextNodes based on markdown image syntax.
    
    Takes a list of TextNodes and splits any TEXT type nodes that contain
    markdown images into multiple nodes with appropriate text types.
    
    Args:
        old_nodes (list): List of TextNode objects to process
        
    Returns:
        list: New list of TextNode objects with split nodes
    """
    new_nodes = []
    
    for node in old_nodes:
        # Only process TEXT type nodes, pass others through unchanged
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        # Extract all images from the node's text
        images = extract_markdown_images(node.text)
        
        # If no images found, add the original node
        if not images:
            new_nodes.append(node)
            continue
        
        # Split the text based on the images found
        current_text = node.text
        
        for alt_text, url in images:
            # Construct the full markdown image syntax to split on
            image_markdown = f"![{alt_text}]({url})"
            
            # Split the current text on this image
            parts = current_text.split(image_markdown, 1)  # Only split on first occurrence
            
            if len(parts) == 2:
                # Add the text before the image (if not empty)
                if parts[0]:
                    new_nodes.append(TextNode(parts[0], TextType.TEXT))
                
                # Add the image node
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                
                # Continue with the remaining text
                current_text = parts[1]
        
        # Add any remaining text after the last image (if not empty)
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    
    return new_nodes

def split_nodes_link(old_nodes):
    """
    Split TextNodes based on markdown link syntax.
    
    Takes a list of TextNodes and splits any TEXT type nodes that contain
    markdown links into multiple nodes with appropriate text types.
    
    Args:
        old_nodes (list): List of TextNode objects to process
        
    Returns:
        list: New list of TextNode objects with split nodes
    """
    new_nodes = []
    
    for node in old_nodes:
        # Only process TEXT type nodes, pass others through unchanged
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        # Extract all links from the node's text
        links = extract_markdown_links(node.text)
        
        # If no links found, add the original node
        if not links:
            new_nodes.append(node)
            continue
        
        # Split the text based on the links found
        current_text = node.text
        
        for anchor_text, url in links:
            # Construct the full markdown link syntax to split on
            link_markdown = f"[{anchor_text}]({url})"
            
            # Split the current text on this link
            parts = current_text.split(link_markdown, 1)  # Only split on first occurrence
            
            if len(parts) == 2:
                # Add the text before the link (if not empty)
                if parts[0]:
                    new_nodes.append(TextNode(parts[0], TextType.TEXT))
                
                # Add the link node
                new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
                
                # Continue with the remaining text
                current_text = parts[1]
        
        # Add any remaining text after the last link (if not empty)
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    
    return new_nodes
