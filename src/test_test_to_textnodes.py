import unittest
from textnode import TextNode, TextType
from text_to_textnodes import text_to_textnodes

class TestTextToTextNodes(unittest.TestCase):
    
    def test_text_to_textnodes_full_example(self):
        """Test the full example from the assignment"""
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        
        self.assertEqual(len(nodes), len(expected))
        for i, (actual, expected_node) in enumerate(zip(nodes, expected)):
            self.assertEqual(actual.text, expected_node.text, f"Mismatch at index {i}: text")
            self.assertEqual(actual.text_type, expected_node.text_type, f"Mismatch at index {i}: text_type")
            self.assertEqual(actual.url, expected_node.url, f"Mismatch at index {i}: url")
    
    def test_text_to_textnodes_plain_text(self):
        """Test plain text with no markdown"""
        text = "This is just plain text with no special formatting"
        nodes = text_to_textnodes(text)
        
        expected = [TextNode("This is just plain text with no special formatting", TextType.TEXT)]
        self.assertEqual(nodes, expected)
    
    def test_text_to_textnodes_only_bold(self):
        """Test text with only bold formatting"""
        text = "This has **bold text** in it"
        nodes = text_to_textnodes(text)
        
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" in it", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)
    
    def test_text_to_textnodes_only_italic(self):
        """Test text with only italic formatting"""
        text = "This has *italic text* in it"
        nodes = text_to_textnodes(text)
        
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" in it", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)
    
    def test_text_to_textnodes_only_code(self):
        """Test text with only code formatting"""
        text = "This has `code text` in it"
        nodes = text_to_textnodes(text)
        
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("code text", TextType.CODE),
            TextNode(" in it", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)
    
    def test_text_to_textnodes_only_image(self):
        """Test text with only an image"""
        text = "This has an ![image](https://example.com/img.png) in it"
        nodes = text_to_textnodes(text)
        
        expected = [
            TextNode("This has an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
            TextNode(" in it", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)
    
    def test_text_to_textnodes_only_link(self):
        """Test text with only a link"""
        text = "This has a [link](https://example.com) in it"
        nodes = text_to_textnodes(text)
        
        expected = [
            TextNode("This has a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" in it", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)
    
    def test_text_to_textnodes_multiple_same_type(self):
        """Test text with multiple instances of the same formatting type"""
        text = "**First bold** and **second bold** text"
        nodes = text_to_textnodes(text)
        
        expected = [
            TextNode("First bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("second bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)
    
    def test_text_to_textnodes_adjacent_formatting(self):
        """Test adjacent formatting with no text between"""
        text = "**bold**`code`*italic*"
        nodes = text_to_textnodes(text)
        
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("code", TextType.CODE),
            TextNode("italic", TextType.ITALIC),
        ]
        self.assertEqual(nodes, expected)
    
    def test_text_to_textnodes_nested_delimiters_not_supported(self):
        """Test that nested delimiters are handled according to our rules (not supported)"""
        # Our implementation processes ** before *, so **bold *and italic* text** would be:
        # - "bold *and italic* text" as BOLD
        text = "This is **bold *and italic* text** here"
        nodes = text_to_textnodes(text)
        
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold *and italic* text", TextType.BOLD),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)
    
    def test_text_to_textnodes_mixed_images_and_links(self):
        """Test text with both images and links"""
        text = "Check out ![this image](https://example.com/img.png) and [this link](https://example.com)"
        nodes = text_to_textnodes(text)
        
        expected = [
            TextNode("Check out ", TextType.TEXT),
            TextNode("this image", TextType.IMAGE, "https://example.com/img.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("this link", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(nodes, expected)
    
    def test_text_to_textnodes_empty_string(self):
        """Test empty string input"""
        text = ""
        nodes = text_to_textnodes(text)
        
        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(nodes, expected)
    
    def test_text_to_textnodes_complex_mixed(self):
        """Test complex text with all types of formatting mixed"""
        text = "Start **bold** then *italic* and `code` with ![img](https://example.com/pic.jpg) plus [link](https://example.com) end"
        nodes = text_to_textnodes(text)
        
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" then ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" with ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "https://example.com/pic.jpg"),
            TextNode(" plus ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" end", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)
    
    def test_text_to_textnodes_at_start_and_end(self):
        """Test formatting at the very start and end of text"""
        text = "**Start bold** middle text *end italic*"
        nodes = text_to_textnodes(text)
        
        expected = [
            TextNode("Start bold", TextType.BOLD),
            TextNode(" middle text ", TextType.TEXT),
            TextNode("end italic", TextType.ITALIC),
        ]
        self.assertEqual(nodes, expected)
    
    def test_text_to_textnodes_only_formatted_text(self):
        """Test text that is entirely formatted (no plain text)"""
        text = "**bold**"
        nodes = text_to_textnodes(text)
        
        expected = [TextNode("bold", TextType.BOLD)]
        self.assertEqual(nodes, expected)
    
    def test_text_to_textnodes_multiple_links_and_images(self):
        """Test multiple links and images"""
        text = "![img1](https://example.com/1.png) and [link1](https://example.com/1) then ![img2](https://example.com/2.png) and [link2](https://example.com/2)"
        nodes = text_to_textnodes(text)
        
        expected = [
            TextNode("img1", TextType.IMAGE, "https://example.com/1.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "https://example.com/1"),
            TextNode(" then ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "https://example.com/2.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "https://example.com/2"),
        ]
        self.assertEqual(nodes, expected)
    
    def test_text_to_textnodes_empty_formatted_text(self):
        """Test truly empty content within formatting"""
        text = "Text with **** empty and `` empty"
        nodes = text_to_textnodes(text)
        
        # The **** should be parsed as empty bold (nothing between **)
        # The `` should be parsed as empty code (nothing between `)
        # Both empty parts should be skipped per our split_nodes_delimiter implementation
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode(" empty and ", TextType.TEXT),
            TextNode(" empty", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)
    
    def test_text_to_textnodes_url_with_special_chars(self):
        """Test URLs with special characters"""
        text = "Link to [API docs](https://api.example.com/v1/docs?format=json&lang=en#overview)"
        nodes = text_to_textnodes(text)
        
        expected = [
            TextNode("Link to ", TextType.TEXT),
            TextNode("API docs", TextType.LINK, "https://api.example.com/v1/docs?format=json&lang=en#overview"),
        ]
        self.assertEqual(nodes, expected)

if __name__ == "__main__":
    unittest.main()
