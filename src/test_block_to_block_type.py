import unittest
from block_to_block_type import block_to_block_type, BlockType

class TestBlockToBlockType(unittest.TestCase):
    
    # Tests for HEADING blocks
    
    def test_heading_h1(self):
        """Test H1 heading"""
        block = "# This is an H1 heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)
    
    def test_heading_h2(self):
        """Test H2 heading"""
        block = "## This is an H2 heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)
    
    def test_heading_h3(self):
        """Test H3 heading"""
        block = "### This is an H3 heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)
    
    def test_heading_h6(self):
        """Test H6 heading (maximum level)"""
        block = "###### This is an H6 heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)
    
    def test_heading_with_formatting(self):
        """Test heading with internal formatting"""
        block = "# This is a heading with **bold** text"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)
    
    def test_not_heading_no_space(self):
        """Test that # without space is not a heading"""
        block = "#This is not a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_not_heading_too_many_hashes(self):
        """Test that more than 6 # is not a heading"""
        block = "####### This is not a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_not_heading_hash_in_middle(self):
        """Test that # in middle of line is not a heading"""
        block = "This # is not a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    # Tests for CODE blocks
    
    def test_code_block_simple(self):
        """Test simple code block"""
        block = "```\nprint('Hello, world!')\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)
    
    def test_code_block_with_language(self):
        """Test code block with language specification"""
        block = "```python\ndef hello():\n    print('Hello!')\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)
    
    def test_code_block_multiline(self):
        """Test multiline code block"""
        block = """```
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```"""
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)
    
    def test_not_code_block_no_end(self):
        """Test that ``` without ending ``` is not a code block"""
        block = "```\nprint('Hello')"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_not_code_block_no_start(self):
        """Test that ``` only at end is not a code block"""
        block = "print('Hello')\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_not_code_block_just_backticks(self):
        """Test that just ``` is not a code block"""
        block = "```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    # Tests for QUOTE blocks
    
    def test_quote_single_line(self):
        """Test single line quote"""
        block = "> This is a quote"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)
    
    def test_quote_multiline(self):
        """Test multiline quote"""
        block = "> This is a quote\n> that spans multiple\n> lines"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)
    
    def test_quote_with_formatting(self):
        """Test quote with internal formatting"""
        block = "> This is a **bold** quote\n> with _italic_ text"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)
    
    def test_quote_empty_lines(self):
        """Test quote with empty quote lines"""
        block = "> This is a quote\n>\n> with an empty line"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)
    
    def test_not_quote_missing_marker(self):
        """Test that missing > on one line makes it not a quote"""
        block = "> This is a quote\nThis line breaks it\n> Back to quote"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    # Tests for UNORDERED_LIST blocks
    
    def test_unordered_list_single_item(self):
        """Test single item unordered list"""
        block = "- Single item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)
    
    def test_unordered_list_multiple_items(self):
        """Test multiple item unordered list"""
        block = "- First item\n- Second item\n- Third item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)
    
    def test_unordered_list_with_formatting(self):
        """Test unordered list with internal formatting"""
        block = "- Item with **bold** text\n- Item with _italic_ text\n- Item with `code`"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)
    
    def test_not_unordered_list_no_space(self):
        """Test that - without space is not an unordered list"""
        block = "-No space\n-Still no space"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_not_unordered_list_missing_marker(self):
        """Test that missing - on one line makes it not an unordered list"""
        block = "- First item\nSecond item without marker\n- Third item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    # Tests for ORDERED_LIST blocks
    
    def test_ordered_list_single_item(self):
        """Test single item ordered list"""
        block = "1. Single item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)
    
    def test_ordered_list_multiple_items(self):
        """Test multiple item ordered list"""
        block = "1. First item\n2. Second item\n3. Third item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)
    
    def test_ordered_list_long(self):
        """Test longer ordered list"""
        block = "1. First\n2. Second\n3. Third\n4. Fourth\n5. Fifth"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)
    
    def test_ordered_list_with_formatting(self):
        """Test ordered list with internal formatting"""
        block = "1. Item with **bold** text\n2. Item with _italic_ text\n3. Item with `code`"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)
    
    def test_not_ordered_list_wrong_start(self):
        """Test that starting with number other than 1 is not an ordered list"""
        block = "2. Second item\n3. Third item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_not_ordered_list_skipped_number(self):
        """Test that skipping a number makes it not an ordered list"""
        block = "1. First item\n3. Third item\n4. Fourth item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_not_ordered_list_no_space(self):
        """Test that number. without space is not an ordered list"""
        block = "1.No space\n2.Still no space"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_not_ordered_list_wrong_format(self):
        """Test that wrong format is not an ordered list"""
        block = "1) First item\n2) Second item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    # Tests for PARAGRAPH blocks
    
    def test_paragraph_simple(self):
        """Test simple paragraph"""
        block = "This is a simple paragraph."
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_paragraph_multiline(self):
        """Test multiline paragraph"""
        block = "This is a paragraph\nthat spans multiple lines\nwithout any special formatting."
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_paragraph_with_formatting(self):
        """Test paragraph with inline formatting"""
        block = "This paragraph has **bold** and _italic_ and `code` formatting."
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_paragraph_with_links(self):
        """Test paragraph with links and images"""
        block = "Check out ![this image](https://example.com/img.png) and [this link](https://example.com)."
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_paragraph_empty_string(self):
        """Test empty string defaults to paragraph"""
        block = ""
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_paragraph_special_characters(self):
        """Test paragraph with special characters that might look like other block types"""
        block = "This has # in the middle and > also in middle and - not at start"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    # Edge case tests
    
    def test_mixed_content_not_valid_blocks(self):
        """Test that mixed content that doesn't match rules becomes paragraph"""
        block = "> Quote line\nNormal line\n- List item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_code_block_backticks_in_middle(self):
        """Test that backticks in middle don't make it a code block"""
        block = "This has ```code``` in the middle"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_heading_multiline_not_heading(self):
        """Test that multiline text starting with # is not all headings"""
        block = "# This looks like a heading\nBut this line makes it a paragraph"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_ordered_list_with_letters(self):
        """Test that letters instead of numbers is not an ordered list"""
        block = "a. First item\nb. Second item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_quote_with_space_after_marker(self):
        """Test quote with extra space after >"""
        block = ">  This is a quote with extra space"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)

if __name__ == "__main__":
    unittest.main()
