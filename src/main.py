import os
import shutil
import sys

from markdown_to_html_node import markdown_to_html_node

def copy_static_to_public(source_dir, dest_dir):
    """
    Recursively copy all contents from source directory to destination directory.
    
    Args:
        source_dir (str): Path to the source directory (e.g., 'static')
        dest_dir (str): Path to the destination directory (e.g., 'docs')
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

def generate_page(from_path, template_path, dest_path, basepath="/"):
    """
    Generate an HTML page from markdown using a template.
    
    Args:
        from_path (str): Path to the markdown file
        template_path (str): Path to the HTML template file
        dest_path (str): Path where the generated HTML should be written
        basepath (str): Base path for the site (e.g., "/" or "/repo-name/")
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read the markdown file
    with open(from_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Read the template file
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    # Extract title from markdown
    page_title = extract_title(markdown_content)
    
    # Replace placeholders in template
    final_html = template_content.replace("{{ Title }}", page_title).replace("{{ Content }}", html_content)
    
    # Fix paths for GitHub Pages deployment
    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')
    
    # Create destination directory if it doesn't exist
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    # Write the final HTML to the destination file
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"Page generated at {dest_path}")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    """
    Recursively generate HTML pages from markdown files in a directory structure.
    
    Crawls every entry in the content directory and generates HTML files for each
    markdown file found, maintaining the same directory structure in the destination.
    
    Args:
        dir_path_content (str): Path to the content directory containing markdown files
        template_path (str): Path to the HTML template file
        dest_dir_path (str): Path to the destination directory for generated HTML files
        basepath (str): Base path for the site (e.g., "/" or "/repo-name/")
    """
    # Ensure the destination directory exists
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)
    
    # Get all items in the content directory
    for item in os.listdir(dir_path_content):
        content_item_path = os.path.join(dir_path_content, item)
        dest_item_path = os.path.join(dest_dir_path, item)
        
        if os.path.isfile(content_item_path):
            # If it's a markdown file, generate HTML
            if content_item_path.endswith('.md'):
                # Convert .md extension to .html for destination
                html_dest_path = dest_item_path.replace('.md', '.html')
                generate_page(content_item_path, template_path, html_dest_path, basepath)
        elif os.path.isdir(content_item_path):
            # If it's a directory, create the corresponding directory in dest and recurse
            generate_pages_recursive(content_item_path, template_path, dest_item_path, basepath)

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
    
    # Get basepath from command line argument, default to "/"
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    
    print(f"Using basepath: {basepath}")
    
    # Define source and destination directories (relative to project root)
    static_dir = "static"
    dest_dir = "docs"  # Changed from "public" to "docs" for GitHub Pages
    content_dir = "content"
    template_path = "template.html"
    
    # Copy static files to destination directory
    copy_static_to_public(static_dir, dest_dir)
    
    # Generate all pages recursively from content directory
    generate_pages_recursive(content_dir, template_path, dest_dir, basepath)
    
    print("Static site generation complete!")

if __name__ == "__main__":
    main()
