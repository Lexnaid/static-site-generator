from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextNode, TextType
from text_node_to_html import text_node_to_html_node
from text_to_textnodes import text_to_textnodes
from markdown_to_blocks import markdown_to_blocks
from block_to_block_type import block_to_block_type, BlockType

def markdown_to_html_node(markdown):
    """
    Convert a full markdown document into a single parent HTMLNode.
    
    Args:
        markdown (str): Full markdown document as string
        
    Returns:
        ParentNode: A div containing all the converted markdown blocks as children
    """
    # Split markdown into blocks
    blocks = markdown_to_blocks(markdown)
    
    # Convert each block to an HTMLNode
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        block_node = block_to_html_node(block, block_type)
        block_nodes.append(block_node)
    
    # Wrap all blocks in a div
    return ParentNode("div", block_nodes)

def block_to_html_node(block, block_type):
    """
    Convert a single markdown block to an HTMLNode based on its type.
    
    Args:
        block (str): The markdown block text
        block_type (BlockType): The type of the block
        
    Returns:
        HTMLNode: The converted block as an HTMLNode
    """
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    elif block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    elif block_type == BlockType.CODE:
        return code_block_to_html_node(block)
    elif block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    elif block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    else:
        raise ValueError(f"Unsupported block type: {block_type}")

def text_to_children(text):
    """
    Convert text with inline markdown to a list of HTMLNode children.
    
    Args:
        text (str): Text that may contain inline markdown
        
    Returns:
        list: List of HTMLNode objects representing the inline content
    """
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def text_to_children_inline(text):
    """
    Convert text with inline markdown to a list of HTMLNode children.
    Converts newlines to spaces for inline content like paragraphs and headings.
    
    Args:
        text (str): Text that may contain inline markdown
        
    Returns:
        list: List of HTMLNode objects representing the inline content
    """
    # Replace newlines with spaces for inline content (paragraphs, headings, etc.)
    text = text.replace('\n', ' ')
    return text_to_children(text)

def paragraph_to_html_node(block):
    """Convert a paragraph block to a <p> HTMLNode."""
    children = text_to_children_inline(block)
    return ParentNode("p", children)

def heading_to_html_node(block):
    """Convert a heading block to an <h1>-<h6> HTMLNode."""
    # Count the number of # characters
    level = 0
    for char in block:
        if char == '#':
            level += 1
        else:
            break
    
    # Extract the heading text (after "# ")
    heading_text = block[level + 1:]  # +1 to skip the space after #
    children = text_to_children_inline(heading_text)
    
    tag = f"h{level}"
    return ParentNode(tag, children)

def code_block_to_html_node(block):
    """Convert a code block to a <pre><code> HTMLNode."""
    # Remove the ``` from start and end
    code_content = block[3:-3]  # Remove first 3 and last 3 characters
    
    # Strip only leading newline if it exists (from block splitting)
    # but preserve trailing newlines and internal structure
    if code_content.startswith('\n'):
        code_content = code_content[1:]
    
    # Code blocks should not parse inline markdown and should preserve newlines
    code_text_node = TextNode(code_content, TextType.TEXT)
    code_leaf_node = text_node_to_html_node(code_text_node)
    
    # Wrap in <code> then <pre>
    code_node = ParentNode("code", [code_leaf_node])
    return ParentNode("pre", [code_node])

def quote_to_html_node(block):
    """Convert a quote block to a <blockquote> HTMLNode."""
    lines = block.split('\n')
    # Remove the '> ' from each line
    quote_lines = []
    for line in lines:
        if line.startswith('> '):
            quote_lines.append(line[2:])  # Remove '> '
        elif line.startswith('>'):
            quote_lines.append(line[1:])  # Remove '>' (for empty quote lines)
    
    # Join lines back together
    quote_text = '\n'.join(quote_lines)
    children = text_to_children(quote_text)
    
    return ParentNode("blockquote", children)

def unordered_list_to_html_node(block):
    """Convert an unordered list block to a <ul> HTMLNode."""
    lines = block.split('\n')
    list_items = []
    
    for line in lines:
        # Remove the '- ' from each line
        item_text = line[2:].strip()  # Remove '- ' and strip extra whitespace
        item_children = text_to_children_inline(item_text)
        list_item = ParentNode("li", item_children)
        list_items.append(list_item)
    
    return ParentNode("ul", list_items)

def ordered_list_to_html_node(block):
    """Convert an ordered list block to an <ol> HTMLNode."""
    lines = block.split('\n')
    list_items = []
    
    for line in lines:
        # Find the '. ' and remove everything up to and including it
        dot_index = line.find('. ')
        item_text = line[dot_index + 2:].strip()  # Remove 'N. ' and strip extra whitespace
        item_children = text_to_children_inline(item_text)
        list_item = ParentNode("li", item_children)
        list_items.append(list_item)
    
    return ParentNode("ol", list_items)
