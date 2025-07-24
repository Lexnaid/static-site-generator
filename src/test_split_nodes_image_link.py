import unittest
from textnode import TextNode, TextType
from split_nodes_image_link import split_nodes_image, split_nodes_link

class TestSplitNodesImageLink(unittest.TestCase):
    
    # Tests for split_nodes_image
    
    def test_split_images(self):
        """Test splitting nodes with multiple images (from assignment)"""
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ]
        self.assertListEqual(expected, new_nodes)
    
    def test_split_images_single(self):
        """Test splitting node with single image"""
        node = TextNode(
            "Check out this ![cool pic](https://example.com/pic.jpg) image!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Check out this ", TextType.TEXT),
            TextNode("cool pic", TextType.IMAGE, "https://example.com/pic.jpg"),
            TextNode(" image!", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)
    
    def test_split_images_at_start(self):
        """Test image at the start of text"""
        node = TextNode(
            "![start image](https://example.com/start.png) followed by text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("start image", TextType.IMAGE, "https://example.com/start.png"),
            TextNode(" followed by text", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)
    
    def test_split_images_at_end(self):
        """Test image at the end of text"""
        node = TextNode(
            "Text before ![end image](https://example.com/end.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Text before ", TextType.TEXT),
            TextNode("end image", TextType.IMAGE, "https://example.com/end.png"),
        ]
        self.assertListEqual(expected, new_nodes)
    
    def test_split_images_only_image(self):
        """Test node containing only an image"""
        node = TextNode(
            "![only image](https://example.com/only.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("only image", TextType.IMAGE, "https://example.com/only.png"),
        ]
        self.assertListEqual(expected, new_nodes)
    
    def test_split_images_no_images(self):
        """Test text with no images"""
        node = TextNode("Just plain text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [node]  # Should return original node unchanged
        self.assertListEqual(expected, new_nodes)
    
    def test_split_images_empty_alt_text(self):
        """Test image with empty alt text"""
        node = TextNode(
            "Image with empty alt: ![](https://example.com/empty.png) here",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Image with empty alt: ", TextType.TEXT),
            TextNode("", TextType.IMAGE, "https://example.com/empty.png"),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)
    
    def test_split_images_adjacent(self):
        """Test adjacent images with no text between"""
        node = TextNode(
            "![first](https://example.com/1.png)![second](https://example.com/2.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("first", TextType.IMAGE, "https://example.com/1.png"),
            TextNode("second", TextType.IMAGE, "https://example.com/2.png"),
        ]
        self.assertListEqual(expected, new_nodes)
    
    def test_split_images_multiple_nodes(self):
        """Test processing multiple input nodes"""
        nodes = [
            TextNode("First ![img1](https://example.com/1.png) node", TextType.TEXT),
            TextNode("Already an image", TextType.IMAGE, "https://example.com/existing.png"),
            TextNode("Second ![img2](https://example.com/2.png) node", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("img1", TextType.IMAGE, "https://example.com/1.png"),
            TextNode(" node", TextType.TEXT),
            TextNode("Already an image", TextType.IMAGE, "https://example.com/existing.png"),  # Unchanged
            TextNode("Second ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "https://example.com/2.png"),
            TextNode(" node", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)
    
    def test_split_images_non_text_nodes_unchanged(self):
        """Test that non-TEXT nodes pass through unchanged"""
        nodes = [
            TextNode("Bold text", TextType.BOLD),
            TextNode("Link text", TextType.LINK, "https://example.com"),
            TextNode("Code text", TextType.CODE),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(nodes, new_nodes)  # Should be unchanged
    
    # Tests for split_nodes_link
    
    def test_split_links_multiple(self):
        """Test splitting node with multiple links (from assignment example)"""
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertListEqual(expected, new_nodes)
    
    def test_split_links_single(self):
        """Test splitting node with single link"""
        node = TextNode(
            "Check out [this website](https://example.com) for more info",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Check out ", TextType.TEXT),
            TextNode("this website", TextType.LINK, "https://example.com"),
            TextNode(" for more info", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)
    
    def test_split_links_at_start(self):
        """Test link at the start of text"""
        node = TextNode(
            "[Start link](https://example.com/start) followed by text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Start link", TextType.LINK, "https://example.com/start"),
            TextNode(" followed by text", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)
    
    def test_split_links_at_end(self):
        """Test link at the end of text"""
        node = TextNode(
            "Text before [end link](https://example.com/end)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Text before ", TextType.TEXT),
            TextNode("end link", TextType.LINK, "https://example.com/end"),
        ]
        self.assertListEqual(expected, new_nodes)
    
    def test_split_links_only_link(self):
        """Test node containing only a link"""
        node = TextNode(
            "[only link](https://example.com/only)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("only link", TextType.LINK, "https://example.com/only"),
        ]
        self.assertListEqual(expected, new_nodes)
    
    def test_split_links_no_links(self):
        """Test text with no links"""
        node = TextNode("Just plain text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [node]  # Should return original node unchanged
        self.assertListEqual(expected, new_nodes)
    
    def test_split_links_empty_anchor_text(self):
        """Test link with empty anchor text"""
        node = TextNode(
            "Link with empty text: [](https://example.com/empty) here",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Link with empty text: ", TextType.TEXT),
            TextNode("", TextType.LINK, "https://example.com/empty"),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)
    
    def test_split_links_adjacent(self):
        """Test adjacent links with no text between"""
        node = TextNode(
            "[first](https://example.com/1)[second](https://example.com/2)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("first", TextType.LINK, "https://example.com/1"),
            TextNode("second", TextType.LINK, "https://example.com/2"),
        ]
        self.assertListEqual(expected, new_nodes)
    
    def test_split_links_relative_urls(self):
        """Test links with relative URLs"""
        node = TextNode(
            "Visit [about page](/about) and [contact](/contact.html)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Visit ", TextType.TEXT),
            TextNode("about page", TextType.LINK, "/about"),
            TextNode(" and ", TextType.TEXT),
            TextNode("contact", TextType.LINK, "/contact.html"),
        ]
        self.assertListEqual(expected, new_nodes)
    
    def test_split_links_multiple_nodes(self):
        """Test processing multiple input nodes"""
        nodes = [
            TextNode("First [link1](https://example.com/1) node", TextType.TEXT),
            TextNode("Already a link", TextType.LINK, "https://example.com/existing"),
            TextNode("Second [link2](https://example.com/2) node", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "https://example.com/1"),
            TextNode(" node", TextType.TEXT),
            TextNode("Already a link", TextType.LINK, "https://example.com/existing"),  # Unchanged
            TextNode("Second ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "https://example.com/2"),
            TextNode(" node", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)
    
    def test_split_links_non_text_nodes_unchanged(self):
        """Test that non-TEXT nodes pass through unchanged"""
        nodes = [
            TextNode("Bold text", TextType.BOLD),
            TextNode("Image alt", TextType.IMAGE, "https://example.com/img.png"),
            TextNode("Code text", TextType.CODE),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(nodes, new_nodes)  # Should be unchanged
    
    def test_split_links_ignores_images(self):
        """Test that image syntax is not processed as links"""
        node = TextNode(
            "This ![image](https://example.com/img.png) should not become a link",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [node]  # Should remain unchanged since no links found
        self.assertListEqual(expected, new_nodes)
    
    # Mixed tests
    
    def test_split_images_ignores_links(self):
        """Test that link syntax is not processed as images"""
        node = TextNode(
            "This [link](https://example.com) should not become an image",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [node]  # Should remain unchanged since no images found
        self.assertListEqual(expected, new_nodes)
    
    def test_empty_input_lists(self):
        """Test both functions with empty input lists"""
        self.assertListEqual([], split_nodes_image([]))
        self.assertListEqual([], split_nodes_link([]))
    
    def test_complex_urls_with_params(self):
        """Test with complex URLs containing parameters and fragments"""
        # Test image with complex URL
        node_img = TextNode(
            "![API diagram](https://api.example.com/docs/diagram.png?version=v2&format=svg#overview)",
            TextType.TEXT,
        )
        new_nodes_img = split_nodes_image([node_img])
        expected_img = [
            TextNode("API diagram", TextType.IMAGE, "https://api.example.com/docs/diagram.png?version=v2&format=svg#overview"),
        ]
        self.assertListEqual(expected_img, new_nodes_img)
        
        # Test link with complex URL
        node_link = TextNode(
            "[GitHub repo](https://github.com/user/repo-name?tab=readme#installation)",
            TextType.TEXT,
        )
        new_nodes_link = split_nodes_link([node_link])
        expected_link = [
            TextNode("GitHub repo", TextType.LINK, "https://github.com/user/repo-name?tab=readme#installation"),
        ]
        self.assertListEqual(expected_link, new_nodes_link)

if __name__ == "__main__":
    unittest.main()
