import unittest
from markdown_to_html_node import markdown_to_html_node

class TestMarkdownToHTMLNode(unittest.TestCase):
    
    def test_paragraphs(self):
        """Test paragraph conversion (from assignment)"""
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
    
    def test_codeblock(self):
        """Test code block conversion (from assignment)"""
        md = """
```
This is text that *should* remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that *should* remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_headings(self):
        """Test heading conversion"""
        md = """# Heading 1

## Heading 2

### Heading 3 with **bold** text

#### Heading 4

##### Heading 5

###### Heading 6"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3 with <b>bold</b> text</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6></div>"
        self.assertEqual(html, expected)
    
    def test_quote_block(self):
        """Test quote block conversion"""
        md = """> This is a quote
> that spans multiple lines
> and has **bold** text"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><blockquote>This is a quote\nthat spans multiple lines\nand has <b>bold</b> text</blockquote></div>"
        self.assertEqual(html, expected)
    
    def test_unordered_list(self):
        """Test unordered list conversion"""
        md = """- First item with **bold**
- Second item with *italic*
- Third item with `code`"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><ul><li>First item with <b>bold</b></li><li>Second item with <i>italic</i></li><li>Third item with <code>code</code></li></ul></div>"
        self.assertEqual(html, expected)
    
    def test_ordered_list(self):
        """Test ordered list conversion"""
        md = """1. First numbered item
2. Second item with **formatting**
3. Third item with [link](https://example.com)"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = '<div><ol><li>First numbered item</li><li>Second item with <b>formatting</b></li><li>Third item with <a href="https://example.com">link</a></li></ol></div>'
        self.assertEqual(html, expected)
    
    def test_mixed_content(self):
        """Test mixed content types"""
        md = """# Main Heading

This is a paragraph with **bold** text.

## Subheading

> This is a quote
> with multiple lines

- Unordered list item
- Another item

1. Ordered list item
2. Second ordered item

```
Code block here
with multiple lines
```

Final paragraph."""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = '<div><h1>Main Heading</h1><p>This is a paragraph with <b>bold</b> text.</p><h2>Subheading</h2><blockquote>This is a quote\nwith multiple lines</blockquote><ul><li>Unordered list item</li><li>Another item</li></ul><ol><li>Ordered list item</li><li>Second ordered item</li></ol><pre><code>Code block here\nwith multiple lines\n</code></pre><p>Final paragraph.</p></div>'
        self.assertEqual(html, expected)
    
    def test_single_paragraph(self):
        """Test single paragraph"""
        md = "Just a simple paragraph with no special formatting."
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><p>Just a simple paragraph with no special formatting.</p></div>"
        self.assertEqual(html, expected)
    
    def test_empty_markdown(self):
        """Test empty markdown"""
        md = ""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div></div>"
        self.assertEqual(html, expected)
    
    def test_paragraph_with_all_inline_elements(self):
        """Test paragraph with all types of inline formatting"""
        md = "This has **bold** and *italic* and `code` and ![image](https://example.com/img.png) and [link](https://example.com)."
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = '<div><p>This has <b>bold</b> and <i>italic</i> and <code>code</code> and <img src="https://example.com/img.png" alt="image"></img> and <a href="https://example.com">link</a>.</p></div>'
        self.assertEqual(html, expected)
    
    def test_nested_lists_not_supported(self):
        """Test that our simple implementation handles basic lists"""
        md = """- First level item
- Another first level item"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><ul><li>First level item</li><li>Another first level item</li></ul></div>"
        self.assertEqual(html, expected)
    
    def test_code_block_with_language(self):
        """Test code block with language specification"""
        md = """```python
def hello():
    print("Hello, world!")
```"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = '<div><pre><code>python\ndef hello():\n    print("Hello, world!")\n</code></pre></div>'
        self.assertEqual(html, expected)
    
    def test_quote_with_empty_lines(self):
        """Test quote block with empty quote lines"""
        md = """> First line
>
> Third line after empty"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><blockquote>First line\n\nThird line after empty</blockquote></div>"
        self.assertEqual(html, expected)
    
    def test_multiple_paragraphs_complex(self):
        """Test multiple paragraphs with complex inline formatting"""
        md = """This is the first paragraph with **bold text** and *italic text*.

This is the second paragraph with `inline code` and a [link to Google](https://google.com).

This is the third paragraph with an ![image](https://example.com/image.png) in it."""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = '<div><p>This is the first paragraph with <b>bold text</b> and <i>italic text</i>.</p><p>This is the second paragraph with <code>inline code</code> and a <a href="https://google.com">link to Google</a>.</p><p>This is the third paragraph with an <img src="https://example.com/image.png" alt="image"></img> in it.</p></div>'
        self.assertEqual(html, expected)
    
    def test_heading_with_inline_formatting(self):
        """Test headings with inline formatting"""
        md = """# Heading with **bold** text

## Another heading with *italic* and `code`"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><h1>Heading with <b>bold</b> text</h1><h2>Another heading with <i>italic</i> and <code>code</code></h2></div>"
        self.assertEqual(html, expected)
    
    def test_long_ordered_list(self):
        """Test longer ordered list"""
        md = """1. First item
2. Second item
3. Third item
4. Fourth item
5. Fifth item"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><ol><li>First item</li><li>Second item</li><li>Third item</li><li>Fourth item</li><li>Fifth item</li></ol></div>"
        self.assertEqual(html, expected)
    
    def test_multiline_code_block(self):
        """Test multiline code block"""
        md = """```
function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n-1) + fibonacci(n-2);
}
```"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = '<div><pre><code>function fibonacci(n) {\n    if (n <= 1) return n;\n    return fibonacci(n-1) + fibonacci(n-2);\n}\n</code></pre></div>'
        self.assertEqual(html, expected)

if __name__ == "__main__":
    unittest.main()
