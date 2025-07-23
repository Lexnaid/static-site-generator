import unittest
from textnode import TextNode, TextType
from text_node_to_html import text_node_to_html_node
from leafnode import LeafNode

class TestTextNodeToHTMLNode(unittest.TestCase):
    
    def test_text(self):
        """Test conversion of TEXT type TextNode"""
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None)
    
    def test_bold(self):
        """Test conversion of BOLD type TextNode"""
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertEqual(html_node.props, None)
    
    def test_italic(self):
        """Test conversion of ITALIC type TextNode"""
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertEqual(html_node.props, None)
    
    def test_code(self):
        """Test conversion of CODE type TextNode"""
        node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello')")
        self.assertEqual(html_node.props, None)
    
    def test_link(self):
        """Test conversion of LINK type TextNode"""
        node = TextNode("Click me!", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me!")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})
    
    def test_image(self):
        """Test conversion of IMAGE type TextNode"""
        node = TextNode("Alt text for image", TextType.IMAGE, "https://example.com/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example.com/image.jpg", "alt": "Alt text for image"})
    
    def test_link_without_url_raises_error(self):
        """Test that LINK TextNode without URL raises ValueError"""
        node = TextNode("Click me!", TextType.LINK)  # No URL provided
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), "Link TextNode must have a URL")
    
    def test_image_without_url_raises_error(self):
        """Test that IMAGE TextNode without URL raises ValueError"""
        node = TextNode("Alt text", TextType.IMAGE)  # No URL provided
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), "Image TextNode must have a URL")
    
    def test_link_with_none_url_raises_error(self):
        """Test that LINK TextNode with None URL raises ValueError"""
        node = TextNode("Click me!", TextType.LINK, None)
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), "Link TextNode must have a URL")
    
    def test_image_with_none_url_raises_error(self):
        """Test that IMAGE TextNode with None URL raises ValueError"""
        node = TextNode("Alt text", TextType.IMAGE, None)
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), "Image TextNode must have a URL")
    
    def test_to_html_output_text(self):
        """Test that the returned LeafNode produces correct HTML for TEXT"""
        node = TextNode("Just plain text", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "Just plain text")
    
    def test_to_html_output_bold(self):
        """Test that the returned LeafNode produces correct HTML for BOLD"""
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")
    
    def test_to_html_output_link(self):
        """Test that the returned LeafNode produces correct HTML for LINK"""
        node = TextNode("Google", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), '<a href="https://www.google.com">Google</a>')
    
    def test_to_html_output_image(self):
        """Test that the returned LeafNode produces correct HTML for IMAGE"""
        node = TextNode("A beautiful sunset", TextType.IMAGE, "https://example.com/sunset.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), '<img src="https://example.com/sunset.jpg" alt="A beautiful sunset"></img>')
    
    def test_unsupported_text_type_raises_error(self):
        """Test that unsupported TextType raises ValueError"""
        # This test assumes there might be additional TextTypes in the future
        # For now, we'll create a mock TextNode with an invalid type
        node = TextNode("Test", TextType.TEXT)
        node.text_type = "INVALID_TYPE"  # Manually set invalid type
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertIn("Unsupported TextType", str(context.exception))

if __name__ == "__main__":
    unittest.main()
