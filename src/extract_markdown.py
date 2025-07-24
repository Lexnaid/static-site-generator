import re

def extract_markdown_images(text):
    """
    Extract markdown images from text and return a list of tuples.
    
    Args:
        text (str): Raw markdown text to extract images from
        
    Returns:
        list: List of tuples containing (alt_text, url) for each image
        
    Example:
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        extract_markdown_images(text)
        # Returns: [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
    """
    # Regex pattern for markdown images: ![alt text](url)
    # !\[([^\[\]]*)\]\(([^\(\)]*)\)
    # !           - literal exclamation mark
    # \[          - literal opening bracket
    # ([^\[\]]*)  - capture group 1: any characters except [ and ] (alt text)
    # \]          - literal closing bracket
    # \(          - literal opening parenthesis
    # ([^\(\)]*)  - capture group 2: any characters except ( and ) (URL)
    # \)          - literal closing parenthesis
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    """
    Extract markdown links from text and return a list of tuples.
    
    Args:
        text (str): Raw markdown text to extract links from
        
    Returns:
        list: List of tuples containing (anchor_text, url) for each link
        
    Example:
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        extract_markdown_links(text)
        # Returns: [("to boot dev", "https://www.boot.dev")]
    """
    # Regex pattern for markdown links (but not images): [text](url)
    # (?<!\!)     - negative lookbehind: not preceded by !
    # \[          - literal opening bracket
    # ([^\[\]]*)  - capture group 1: any characters except [ and ] (anchor text)
    # \]          - literal closing bracket
    # \(          - literal opening parenthesis
    # ([^\(\)]*)  - capture group 2: any characters except ( and ) (URL)
    # \)          - literal closing parenthesis
    pattern = r"(?<!\!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches
