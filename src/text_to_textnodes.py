from textnode import TextNode, TextType
from split_nodes_delimiter import split_nodes_delimiter
from split_nodes_image_link import split_nodes_image, split_nodes_link

def text_to_textnodes(text):
    """
    Convert raw markdown text into a list of TextNode objects.
    
    Takes a string of markdown-flavored text and splits it into TextNodes
    based on various markdown syntax including bold, italic, code, images, and links.
    
    Args:
        text (str): Raw markdown text to convert
        
    Returns:
        list: List of TextNode objects representing the parsed markdown
        
    Example:
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        # Returns list of TextNodes with appropriate types and URLs
    """
    # Start with a single TEXT node containing all the text
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Apply all the splitting functions in sequence
    # Order matters here - we want to process in a logical sequence
    
    # 1. Split images first (![alt](url)) - they contain brackets that could interfere with links
    nodes = split_nodes_image(nodes)
    
    # 2. Split links ([text](url))
    nodes = split_nodes_link(nodes)
    
    # 3. Split code text (`text`) - do this before bold/italic to avoid conflicts with backticks
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    # 4. Split bold text (**text**) - do this before italic to handle ** vs * properly
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    
    # 5. Split italic text (*text*) - do this last for * to avoid conflicts with **
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)


    return nodes
