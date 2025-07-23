import os
import shutil

from markdown_to_html import markdown_to_html_node  # Assuming this is a custom module for markdown conversion

def copy_static_to_public(source_dir, dest_dir):
    """
    Recursively copy all contents from source directory to destination directory.
    
    Args:
        source_dir (str): Path to the source directory (e.g., 'static')
        dest_dir (str): Path to the destination directory (e.g., 'public')
    """
    # First, clean the destination directory
    if os.path.exists(dest_dir):
        print(f"Deleting existing directory: {dest_dir}")
        shutil.rmtree(dest_dir)
    
    # Create the destination directory
    print(f"Creating directory: {dest_dir}")
    os.mkdir(dest_dir)
    
    # Copy contents recursively
    _copy_directory_contents(source_dir, dest_dir)

def _copy_directory_contents(source_dir, dest_dir):
    """
    Helper function to recursively copy directory contents.
    
    Args:
        source_dir (str): Source directory path
        dest_dir (str): Destination directory path
    """
    # Check if source directory exists
    if not os.path.exists(source_dir):
        print(f"Source directory does not exist: {source_dir}")
        return
    
    # List all items in the source directory
    items = os.listdir(source_dir)
    
    for item in items:
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)
        
        if os.path.isfile(source_path):
            # Copy file
            print(f"Copying file: {source_path} -> {dest_path}")
            shutil.copy(source_path, dest_path)
        else:
            # It's a directory, create it and copy contents recursively
            print(f"Creating directory: {dest_path}")
            os.mkdir(dest_path)
            _copy_directory_contents(source_path, dest_path)

def generate_page(from_path,template_path, to_path):
    print(f"Generating page from {from_path} using template {template_path} to {to_path}")
    with open(from_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Convert markdown to HTML (this is a placeholder, actual conversion logic needed)

    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    # Extract title from markdown_content

    page_title = extract_title(markdown_content)


    final_html = template_content.replace("{{ html_content }}", html_content).replace("{{ page_title }}", page_title)

    dest_dir = os.path.dirname(to_path)
    if not os.path.exists(dest_dir) and dest_dir:
        os.makedirs(dest_dir)

    with open(to_path, 'w', encoding='utf-8') as f:
        f.write(final_html)


    print(f"Page generated at {to_path}")




def extract_title(markdown):
    """
    Extract the h1 header from a markdown string.
    
    Args:
        markdown (str): The markdown content to extract title from
        
    Returns:
        str: The title text without the # and stripped of whitespace
        
    Raises:
        ValueError: If no h1 header is found
    """
    lines = markdown.split('\n')
    
    for line in lines:
        # Check if line starts with a single # (h1 header)
        if line.startswith('# '):
            # Remove the '# ' and strip whitespace
            title = line[2:].strip()
            if title:  # Make sure there's actual content after the #
                return title
        # Also handle the case where there's just '#' with no space
        elif line.startswith('#') and not line.startswith('##'):
            # Remove the '#' and strip whitespace
            title = line[1:].strip()
            if title:  # Make sure there's actual content after the #
                return title
    
    # If no h1 header found, raise an exception
    raise ValueError("No h1 header found in markdown content")

def main():
    """
    Main function for the static site generator.
    """
    print("Starting static site generator...")
    
    # Define source and destination directories (relative to project root)
    static_dir = "static"
    public_dir = "public"
    
    # Copy static files to public directory
    copy_static_to_public(static_dir, public_dir)
    
    print("Static site generation complete!")

if __name__ == "__main__":
    main()
