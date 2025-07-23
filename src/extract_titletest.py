import unittest
from main import extract_title

class TestExtractTitle(unittest.TestCase):
    
    def test_extract_title_simple(self):
        """Test extracting a simple h1 title"""
        markdown = "# Hello"
        result = extract_title(markdown)
        self.assertEqual(result, "Hello")
    
    def test_extract_title_with_content(self):
        """Test extracting title from markdown with other content"""
        markdown = """# Tolkien Fan Club

Some content here.

## Subtitle

More content."""
        result = extract_title(markdown)
        self.assertEqual(result, "Tolkien Fan Club")
    
    def test_extract_title_with_extra_whitespace(self):
        """Test extracting title with extra whitespace"""
        markdown = "#   Spaced Title   "
        result = extract_title(markdown)
        self.assertEqual(result, "Spaced Title")
    
    def test_extract_title_with_space_after_hash(self):
        """Test extracting title with proper space after #"""
        markdown = "# Proper Title"
        result = extract_title(markdown)
        self.assertEqual(result, "Proper Title")
    
    def test_extract_title_multiline_before(self):
        """Test extracting title when h1 is not the first line"""
        markdown = """Some intro text

# The Real Title

Content follows."""
        result = extract_title(markdown)
        self.assertEqual(result, "The Real Title")
    
    def test_extract_title_ignores_h2(self):
        """Test that h2 headers are ignored when looking for h1"""
        markdown = """## This is H2

# This is H1

### This is H3"""
        result = extract_title(markdown)
        self.assertEqual(result, "This is H1")
    
    def test_extract_title_ignores_h3_and_higher(self):
        """Test that h3+ headers are ignored"""
        markdown = """### H3 Header
#### H4 Header
# Real Title
##### H5 Header"""
        result = extract_title(markdown)
        self.assertEqual(result, "Real Title")
    
    def test_extract_title_first_h1_wins(self):
        """Test that the first h1 header is returned when multiple exist"""
        markdown = """# First Title

Some content

# Second Title"""
        result = extract_title(markdown)
        self.assertEqual(result, "First Title")
    
    def test_extract_title_no_h1_raises_error(self):
        """Test that missing h1 header raises ValueError"""
        markdown = """## Only H2 Here

### And H3

Some content without h1."""
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No h1 header found in markdown content")
    
    def test_extract_title_empty_h1_raises_error(self):
        """Test that empty h1 header raises ValueError"""
        markdown = "#   "
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No h1 header found in markdown content")
    
    def test_extract_title_only_hash_raises_error(self):
        """Test that just # with no content raises ValueError"""
        markdown = "#"
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No h1 header found in markdown content")
    
    def test_extract_title_empty_string_raises_error(self):
        """Test that empty markdown raises ValueError"""
        markdown = ""
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No h1 header found in markdown content")
    
    def test_extract_title_complex_title(self):
        """Test extracting title with special characters and numbers"""
        markdown = "# The Lord of the Rings: Book 1 - Chapter 10!"
        result = extract_title(markdown)
        self.assertEqual(result, "The Lord of the Rings: Book 1 - Chapter 10!")
    
    def test_extract_title_with_inline_code(self):
        """Test extracting title that contains inline code"""
        markdown = "# How to Use `git commit`"
        result = extract_title(markdown)
        self.assertEqual(result, "How to Use `git commit`")

if __name__ == "__main__":
    unittest.main()
