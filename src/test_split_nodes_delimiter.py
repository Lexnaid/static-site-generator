import unittest
from textnode import TextNode, TextType
from split_nodes_delimiter import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    
    def test_split_code_delimiter(self):
        """Test splitting with code delimiter (backtick)"""
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        
        self.assertEqual(len(new_nodes), 3)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)
    
    def test_split_bold_delimiter(self):
        """Test splitting with bold delimiter (**)"""
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
        ]
        
        self.assertEqual(len(new_nodes), 3)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)
    
    def test_split_italic_delimiter(self):
        """Test splitting with italic delimiter (*)"""
        node = TextNode("This is *italic text* here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" here", TextType.TEXT),
        ]
        
        self.assertEqual(len(new_nodes), 3)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)
    
    def test_multiple_delimiters(self):
        """Test text with multiple pairs of delimiters"""
        node = TextNode("This has `code` and `more code` in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("more code", TextType.CODE),
            TextNode(" in it", TextType.TEXT),
        ]
        
        self.assertEqual(len(new_nodes), 5)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)
    
    def test_no_delimiter_in_text(self):
        """Test text with no delimiters (should return unchanged)"""
        node = TextNode("This is just plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is just plain text")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
    
    def test_delimiter_at_start_and_end(self):
        """Test text that starts and ends with delimiters"""
        node = TextNode("`start code` middle `end code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("start code", TextType.CODE),
            TextNode(" middle ", TextType.TEXT),
            TextNode("end code", TextType.CODE),
        ]
        
        self.assertEqual(len(new_nodes), 3)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)
    
    def test_entire_text_is_delimiter_content(self):
        """Test when entire text is wrapped in delimiters"""
        node = TextNode("`entire text is code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "entire text is code")
        self.assertEqual(new_nodes[0].text_type, TextType.CODE)
    
    def test_empty_delimiter_content(self):
        """Test delimiters with empty content between them"""
        node = TextNode("Text with `` empty code", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        # Empty parts should be skipped
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode(" empty code", TextType.TEXT),
        ]
        
        self.assertEqual(len(new_nodes), 2)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)
    
    def test_unmatched_delimiter_raises_error(self):
        """Test that unmatched delimiters raise ValueError"""
        node = TextNode("This has `unmatched delimiter", TextType.TEXT)
        
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        
        self.assertIn("Unmatched delimiter", str(context.exception))
    
    def test_multiple_nodes_input(self):
        """Test processing multiple nodes in input list"""
        nodes = [
            TextNode("First `code` text", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),  # Should pass through unchanged
            TextNode("Second `more code` text", TextType.TEXT),
        ]
        
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),  # Unchanged
            TextNode("Second ", TextType.TEXT),
            TextNode("more code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        
        self.assertEqual(len(new_nodes), 7)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)
    
    def test_non_text_nodes_unchanged(self):
        """Test that non-TEXT nodes pass through unchanged"""
        nodes = [
            TextNode("Bold text", TextType.BOLD),
            TextNode("Italic text", TextType.ITALIC),
            TextNode("Code text", TextType.CODE),
            TextNode("Link text", TextType.LINK, "http://example.com"),
        ]
        
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        
        # All nodes should be unchanged
        self.assertEqual(len(new_nodes), 4)
        for i, original_node in enumerate(nodes):
            self.assertEqual(new_nodes[i].text, original_node.text)
            self.assertEqual(new_nodes[i].text_type, original_node.text_type)
            self.assertEqual(new_nodes[i].url, original_node.url)
    
    def test_empty_input_list(self):
        """Test empty input list"""
        new_nodes = split_nodes_delimiter([], "`", TextType.CODE)
        self.assertEqual(new_nodes, [])
    
    def test_complex_bold_example(self):
        """Test complex bold delimiter example"""
        node = TextNode("Start **bold one** middle **bold two** end", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("bold one", TextType.BOLD),
            TextNode(" middle ", TextType.TEXT),
            TextNode("bold two", TextType.BOLD),
            TextNode(" end", TextType.TEXT),
        ]
        
        self.assertEqual(len(new_nodes), 5)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)
    
    def test_adjacent_delimiters(self):
        """Test adjacent delimiter pairs"""
        node = TextNode("Text with `code1``code2` more text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("code1", TextType.CODE),
            TextNode("code2", TextType.CODE),
            TextNode(" more text", TextType.TEXT),
        ]
        
        self.assertEqual(len(new_nodes), 4)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)

if __name__ == "__main__":
    unittest.main()
