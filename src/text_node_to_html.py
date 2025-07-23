from leafnode import LeafNode
from textnode import TextNode, TextType

def text_node_to_html_node(text_node):
    """
    Convert a TextNode to a LeafNode (HTMLNode).
    
    Args:
        text_node (TextNode): The TextNode to convert
        
    Returns:
        LeafNode: The corresponding LeafNode object
        
    Raises:
        ValueError: If the TextNode has an unsupported TextType
    """
    if text_node.text_type == TextType.TEXT:
        # Raw text with no tag
        return LeafNode(None, text_node.text)
    
    elif text_node.text_type == TextType.BOLD:
        # Bold text with <b> tag
        return LeafNode("b", text_node.text)
    
    elif text_node.text_type == TextType.ITALIC:
        # Italic text with <i> tag
        return LeafNode("i", text_node.text)
    
    elif text_node.text_type == TextType.CODE:
        # Code text with <code> tag
        return LeafNode("code", text_node.text)
    
    elif text_node.text_type == TextType.LINK:
        # Link with <a> tag and href property
        if not text_node.url:
            raise ValueError("Link TextNode must have a URL")
        return LeafNode("a", text_node.text, {"href": text_node.url})
    
    elif text_node.text_type == TextType.IMAGE:
        # Image with <img> tag, empty value, src and alt properties
        if not text_node.url:
            raise ValueError("Image TextNode must have a URL")
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    
    else:
        # Unsupported TextType
        raise ValueError(f"Unsupported TextType: {text_node.text_type}")
