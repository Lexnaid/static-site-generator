import unittest
from markdown_to_blocks import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    
    def test_markdown_to_blocks(self):
        """Test the example from the assignment"""
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_basic(self):
        """Test basic functionality with simple blocks"""
        md = "# Heading\n\nThis is a paragraph.\n\n- List item"
        blocks = markdown_to_blocks(md)
        expected = [
            "# Heading",
            "This is a paragraph.",
            "- List item"
        ]
        self.assertEqual(blocks, expected)
    
    def test_markdown_to_blocks_single_block(self):
        """Test markdown with only one block"""
        md = "This is a single paragraph with no blank lines."
        blocks = markdown_to_blocks(md)
        expected = ["This is a single paragraph with no blank lines."]
        self.assertEqual(blocks, expected)
    
    def test_markdown_to_blocks_multiple_newlines(self):
        """Test markdown with multiple blank lines between blocks"""
        md = "First block\n\n\n\nSecond block\n\n\n\n\nThird block"
        blocks = markdown_to_blocks(md)
        expected = ["First block", "Second block", "Third block"]
        self.assertEqual(blocks, expected)
    
    def test_markdown_to_blocks_leading_trailing_whitespace(self):
        """Test blocks with leading and trailing whitespace"""
        md = "   First block   \n\n  Second block with spaces  \n\n\tThird block with tab\t"
        blocks = markdown_to_blocks(md)
        expected = ["First block", "Second block with spaces", "Third block with tab"]
        self.assertEqual(blocks, expected)
    
    def test_markdown_to_blocks_empty_string(self):
        """Test empty markdown string"""
        md = ""
        blocks = markdown_to_blocks(md)
        expected = []
        self.assertEqual(blocks, expected)
    
    def test_markdown_to_blocks_only_whitespace(self):
        """Test markdown with only whitespace"""
        md = "   \n\n  \t  \n\n   "
        blocks = markdown_to_blocks(md)
        expected = []
        self.assertEqual(blocks, expected)
    
    def test_markdown_to_blocks_preserve_internal_newlines(self):
        """Test that single newlines within blocks are preserved"""
        md = "Line 1\nLine 2\nLine 3\n\nNew block\nWith lines"
        blocks = markdown_to_blocks(md)
        expected = [
            "Line 1\nLine 2\nLine 3",
            "New block\nWith lines"
        ]
        self.assertEqual(blocks, expected)
    
    def test_markdown_to_blocks_complex_example(self):
        """Test a more complex markdown document"""
        md = """# Main Heading

This is an introduction paragraph with some **bold** text.

## Subheading

Here's another paragraph with _italic_ and `code` formatting.
This paragraph continues on multiple lines
without blank lines between them.

### List Section

- First item
- Second item with **bold**
- Third item

Here's a final paragraph after the list."""
        
        blocks = markdown_to_blocks(md)
        expected = [
            "# Main Heading",
            "This is an introduction paragraph with some **bold** text.",
            "## Subheading",
            "Here's another paragraph with _italic_ and `code` formatting.\nThis paragraph continues on multiple lines\nwithout blank lines between them.",
            "### List Section",
            "- First item\n- Second item with **bold**\n- Third item",
            "Here's a final paragraph after the list."
        ]
        self.assertEqual(blocks, expected)
    
    def test_markdown_to_blocks_code_block(self):
        """Test markdown with code blocks"""
        md = """Here's some text.

```python
def hello():
    print("Hello, world!")
```

More text here."""
        
        blocks = markdown_to_blocks(md)
        expected = [
            "Here's some text.",
            "```python\ndef hello():\n    print(\"Hello, world!\")\n```",
            "More text here."
        ]
        self.assertEqual(blocks, expected)
    
    def test_markdown_to_blocks_blockquote(self):
        """Test markdown with blockquotes"""
        md = """Regular paragraph.

> This is a blockquote
> that spans multiple lines
> within the same block.

Another paragraph."""
        
        blocks = markdown_to_blocks(md)
        expected = [
            "Regular paragraph.",
            "> This is a blockquote\n> that spans multiple lines\n> within the same block.",
            "Another paragraph."
        ]
        self.assertEqual(blocks, expected)
    
    def test_markdown_to_blocks_mixed_list_types(self):
        """Test markdown with both ordered and unordered lists"""
        md = """# Lists Example

Unordered list:
- Item A
- Item B

Ordered list:
1. First item
2. Second item
3. Third item

End of document."""
        
        blocks = markdown_to_blocks(md)
        expected = [
            "# Lists Example",
            "Unordered list:\n- Item A\n- Item B",
            "Ordered list:\n1. First item\n2. Second item\n3. Third item",
            "End of document."
        ]
        self.assertEqual(blocks, expected)
    
    def test_markdown_to_blocks_starting_with_newlines(self):
        """Test markdown that starts with newlines"""
        md = "\n\nFirst block\n\nSecond block"
        blocks = markdown_to_blocks(md)
        expected = ["First block", "Second block"]
        self.assertEqual(blocks, expected)
    
    def test_markdown_to_blocks_ending_with_newlines(self):
        """Test markdown that ends with newlines"""
        md = "First block\n\nSecond block\n\n"
        blocks = markdown_to_blocks(md)
        expected = ["First block", "Second block"]
        self.assertEqual(blocks, expected)
    
    def test_markdown_to_blocks_only_newlines(self):
        """Test markdown with only newlines"""
        md = "\n\n\n\n"
        blocks = markdown_to_blocks(md)
        expected = []
        self.assertEqual(blocks, expected)
    
    def test_markdown_to_blocks_mixed_whitespace_in_empty_blocks(self):
        """Test that blocks with only whitespace are removed"""
        md = "First block\n\n   \n\nSecond block\n\n\t\t\n\nThird block"
        blocks = markdown_to_blocks(md)
        expected = ["First block", "Second block", "Third block"]
        self.assertEqual(blocks, expected)

if __name__ == "__main__":
    unittest.main()
