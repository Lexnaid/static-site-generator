import unittest
from parentnode import ParentNode
from leafnode import LeafNode  # Assuming LeafNode is defined in leafnode.py

class TestParentNode(unittest.TestCase):
    
    def test_to_html_with_children(self):
        """Test basic parent node with one child"""
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        """Test nested parent nodes (grandchildren)"""
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_multiple_children(self):
        """Test parent node with multiple children"""
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected)
    
    def test_to_html_with_props(self):
        """Test parent node with properties"""
        child_node = LeafNode("span", "content")
        parent_node = ParentNode("div", [child_node], {"class": "container", "id": "main"})
        result = parent_node.to_html()
        # Since dict order isn't guaranteed, check that both attributes are present
        self.assertTrue(result.startswith('<div'))
        self.assertIn('class="container"', result)
        self.assertIn('id="main"', result)
        self.assertIn('<span>content</span>', result)
        self.assertTrue(result.endswith('</div>'))
    
    def test_to_html_nested_parent_nodes(self):
        """Test deeply nested parent nodes"""
        innermost = LeafNode("strong", "Bold")
        middle = ParentNode("em", [innermost])
        outer = ParentNode("p", [middle])
        root = ParentNode("div", [outer])
        expected = "<div><p><em><strong>Bold</strong></em></p></div>"
        self.assertEqual(root.to_html(), expected)
    
    def test_to_html_mixed_children(self):
        """Test parent node with mix of leaf and parent children"""
        leaf1 = LeafNode("b", "Bold")
        leaf2 = LeafNode(None, " and ")
        nested_leaf = LeafNode("em", "emphasized")
        parent_child = ParentNode("span", [nested_leaf])
        leaf3 = LeafNode(None, " text")
        
        root = ParentNode("p", [leaf1, leaf2, parent_child, leaf3])
        expected = "<p><b>Bold</b> and <span><em>emphasized</em></span> text</p>"
        self.assertEqual(root.to_html(), expected)
    
    def test_to_html_no_tag_raises_error(self):
        """Test that parent node without tag raises ValueError"""
        child = LeafNode("span", "child")
        node = ParentNode(None, [child])
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "Parent nodes must have a tag")
    
    def test_to_html_no_children_raises_error(self):
        """Test that parent node without children raises ValueError"""
        node = ParentNode("div", None)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "Parent nodes must have children")
    
    def test_to_html_empty_children_list(self):
        """Test parent node with empty children list"""
        node = ParentNode("div", [])
        # Should work fine with empty list, just produce empty tags
        self.assertEqual(node.to_html(), "<div></div>")
    
    def test_constructor_no_value(self):
        """Test that ParentNode constructor sets value to None"""
        child = LeafNode("span", "child")
        node = ParentNode("div", [child])
        self.assertIsNone(node.value)
    
    def test_complex_nested_structure(self):
        """Test a complex nested HTML structure"""
        # Create: <article><header><h1>Title</h1></header><main><p>Content <em>emphasized</em> text</p></main></article>
        title = LeafNode("h1", "Title")
        header = ParentNode("header", [title])
        
        em_text = LeafNode("em", "emphasized")
        content = ParentNode("p", [
            LeafNode(None, "Content "),
            em_text,
            LeafNode(None, " text")
        ])
        main = ParentNode("main", [content])
        
        article = ParentNode("article", [header, main])
        
        expected = "<article><header><h1>Title</h1></header><main><p>Content <em>emphasized</em> text</p></main></article>"
        self.assertEqual(article.to_html(), expected)
    
    def test_to_html_with_anchor_children(self):
        """Test parent node containing anchor tags with attributes"""
        link1 = LeafNode("a", "Google", {"href": "https://google.com"})
        link2 = LeafNode("a", "GitHub", {"href": "https://github.com"})
        nav = ParentNode("nav", [link1, LeafNode(None, " | "), link2])
        
        result = nav.to_html()
        expected = '<nav><a href="https://google.com">Google</a> | <a href="https://github.com">GitHub</a></nav>'
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
