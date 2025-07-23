import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    
    def test_leaf_to_html_p(self):
        """Test basic paragraph tag rendering"""
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a_with_props(self):
        """Test anchor tag with href property"""
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
    
    def test_leaf_to_html_b(self):
        """Test bold tag rendering"""
        node = LeafNode("b", "This is bold text.")
        self.assertEqual(node.to_html(), "<b>This is bold text.</b>")
    
    def test_leaf_to_html_i(self):
        """Test italic tag rendering"""
        node = LeafNode("i", "This is italic text.")
        self.assertEqual(node.to_html(), "<i>This is italic text.</i>")
    
    def test_leaf_to_html_span_with_multiple_props(self):
        """Test span tag with multiple properties"""
        node = LeafNode("span", "Styled text", {"class": "highlight", "id": "main-text"})
        result = node.to_html()
        # Since dict order isn't guaranteed in older Python versions, check both possibilities
        expected1 = '<span class="highlight" id="main-text">Styled text</span>'
        expected2 = '<span id="main-text" class="highlight">Styled text</span>'
        self.assertTrue(result == expected1 or result == expected2)
    
    def test_leaf_to_html_no_tag(self):
        """Test leaf node with no tag (raw text)"""
        node = LeafNode(None, "Just plain text")
        self.assertEqual(node.to_html(), "Just plain text")
    
    def test_leaf_to_html_empty_props(self):
        """Test leaf node with empty props dict"""
        node = LeafNode("div", "Content", {})
        self.assertEqual(node.to_html(), "<div>Content</div>")
    
    def test_leaf_to_html_no_value_raises_error(self):
        """Test that leaf node without value raises ValueError"""
        node = LeafNode("p", None)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "All leaf nodes must have a value")
    
    def test_leaf_constructor_no_children(self):
        """Test that LeafNode constructor doesn't accept children"""
        node = LeafNode("p", "Test")
        self.assertIsNone(node.children)
    
    def test_leaf_img_self_closing_style(self):
        """Test img tag (though it's rendered as regular tag in this implementation)"""
        node = LeafNode("img", "", {"src": "image.jpg", "alt": "Test image"})
        result = node.to_html()
        # Check that it contains the required attributes
        self.assertIn('src="image.jpg"', result)
        self.assertIn('alt="Test image"', result)
        self.assertTrue(result.startswith("<img"))
        self.assertTrue(result.endswith("></img>"))

if __name__ == "__main__":
    unittest.main()
