import unittest
from extract_markdown import extract_markdown_images, extract_markdown_links

class TestExtractMarkdown(unittest.TestCase):
    
    # Tests for extract_markdown_images
    
    def test_extract_markdown_images_single(self):
        """Test extracting a single image"""
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_images_multiple(self):
        """Test extracting multiple images"""
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"), 
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertListEqual(expected, matches)
    
    def test_extract_markdown_images_empty_alt_text(self):
        """Test image with empty alt text"""
        text = "Image with empty alt: ![](https://example.com/image.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("", "https://example.com/image.png")], matches)
    
    def test_extract_markdown_images_complex_alt_text(self):
        """Test image with complex alt text containing spaces and special chars"""
        text = "![A beautiful sunset over the ocean!](https://example.com/sunset.jpg)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("A beautiful sunset over the ocean!", "https://example.com/sunset.jpg")], matches)
    
    def test_extract_markdown_images_no_images(self):
        """Test text with no images"""
        text = "This is just plain text with no images"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)
    
    def test_extract_markdown_images_with_links(self):
        """Test that images are extracted but links are ignored"""
        text = "Here's an ![image](https://example.com/img.png) and a [link](https://example.com)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://example.com/img.png")], matches)
    
    def test_extract_markdown_images_malformed(self):
        """Test that our regex handles text with parentheses in alt text"""
        text = "Malformed: ![image(https://example.com/img.png) and !image](https://example.com/img2.png)"
        matches = extract_markdown_images(text)
        # Our regex actually matches this because it allows any chars except [ and ] in alt text
        expected = [("image(https://example.com/img.png) and !image", "https://example.com/img2.png")]
        self.assertListEqual(expected, matches)
    
    def test_extract_markdown_images_truly_malformed(self):
        """Test truly malformed image syntax that is ignored"""
        text = "Broken: ![missing closing bracket(https://example.com/img.png) and !image] with paren instead"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)
    
    def test_extract_markdown_images_nested_brackets(self):
        """Test handling of brackets within alt text (should not work with our regex)"""
        text = "![alt [text] with brackets](https://example.com/img.png)"
        matches = extract_markdown_images(text)
        # Our regex stops at the first closing bracket, so this won't match properly
        self.assertListEqual([], matches)
    
    def test_extract_markdown_images_url_with_params(self):
        """Test image URL with query parameters"""
        text = "![thumbnail](https://example.com/img.png?size=100&format=webp)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("thumbnail", "https://example.com/img.png?size=100&format=webp")], matches)
    
    # Tests for extract_markdown_links
    
    def test_extract_markdown_links_single(self):
        """Test extracting a single link"""
        text = "This is text with a [link](https://www.boot.dev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://www.boot.dev")], matches)
    
    def test_extract_markdown_links_multiple(self):
        """Test extracting multiple links"""
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        expected = [
            ("to boot dev", "https://www.boot.dev"), 
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertListEqual(expected, matches)
    
    def test_extract_markdown_links_empty_text(self):
        """Test link with empty anchor text"""
        text = "Empty link text: [](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("", "https://example.com")], matches)
    
    def test_extract_markdown_links_complex_text(self):
        """Test link with complex anchor text"""
        text = "Check out [Boot.dev - Learn Backend Development!](https://www.boot.dev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("Boot.dev - Learn Backend Development!", "https://www.boot.dev")], matches)
    
    def test_extract_markdown_links_no_links(self):
        """Test text with no links"""
        text = "This is just plain text with no links"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)
    
    def test_extract_markdown_links_with_images(self):
        """Test that links are extracted but images are ignored"""
        text = "Here's a [link](https://example.com) and an ![image](https://example.com/img.png)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://example.com")], matches)
    
    def test_extract_markdown_links_not_images(self):
        """Test that image syntax is not matched as links"""
        text = "This ![image](https://example.com/img.png) should not be a link"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)
    
    def test_extract_markdown_links_malformed(self):
        """Test that our regex handles text with parentheses in anchor text"""
        text = "Malformed: [link(https://example.com) and link](https://example.com/page2)"
        matches = extract_markdown_links(text)
        # Our regex actually matches this because it allows any chars except [ and ] in anchor text
        expected = [("link(https://example.com) and link", "https://example.com/page2")]
        self.assertListEqual(expected, matches)
    
    def test_extract_markdown_links_truly_malformed(self):
        """Test truly malformed link syntax that is ignored"""
        text = "Broken: [missing closing bracket(https://example.com) and link] with paren instead"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)
    
    def test_extract_markdown_links_relative_urls(self):
        """Test links with relative URLs"""
        text = "Internal [about page](/about) and [contact](/contact.html)"
        matches = extract_markdown_links(text)
        expected = [
            ("about page", "/about"),
            ("contact", "/contact.html")
        ]
        self.assertListEqual(expected, matches)
    
    def test_extract_markdown_links_url_with_fragment(self):
        """Test link with URL fragment"""
        text = "Jump to [section 2](#section-2) on this page"
        matches = extract_markdown_links(text)
        self.assertListEqual([("section 2", "#section-2")], matches)
    
    # Mixed tests
    
    def test_extract_both_images_and_links_mixed(self):
        """Test text with both images and links mixed together"""
        text = "Check out this ![cool image](https://example.com/img.png) from [our website](https://example.com) and another ![picture](https://example.com/pic.jpg)"
        
        image_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        
        expected_images = [
            ("cool image", "https://example.com/img.png"),
            ("picture", "https://example.com/pic.jpg")
        ]
        expected_links = [
            ("our website", "https://example.com")
        ]
        
        self.assertListEqual(expected_images, image_matches)
        self.assertListEqual(expected_links, link_matches)
    
    def test_extract_adjacent_image_and_link(self):
        """Test adjacent image and link"""
        text = "![image](https://example.com/img.png)[link](https://example.com)"
        
        image_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        
        self.assertListEqual([("image", "https://example.com/img.png")], image_matches)
        self.assertListEqual([("link", "https://example.com")], link_matches)
    
    def test_extract_empty_string(self):
        """Test both functions with empty string"""
        self.assertListEqual([], extract_markdown_images(""))
        self.assertListEqual([], extract_markdown_links(""))
    
    def test_extract_only_brackets_and_parens(self):
        """Test text with brackets and parentheses but no valid markdown"""
        text = "Some [text] and (parentheses) but no valid markdown links or images"
        
        self.assertListEqual([], extract_markdown_images(text))
        self.assertListEqual([], extract_markdown_links(text))
    
    def test_extract_complex_urls(self):
        """Test with complex URLs containing various characters"""
        text = "![API docs](https://api.example.com/v1/docs?lang=en&format=json#overview) and [GitHub repo](https://github.com/user/repo-name_v2)"
        
        image_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        
        expected_images = [("API docs", "https://api.example.com/v1/docs?lang=en&format=json#overview")]
        expected_links = [("GitHub repo", "https://github.com/user/repo-name_v2")]
        
        self.assertListEqual(expected_images, image_matches)
        self.assertListEqual(expected_links, link_matches)

if __name__ == "__main__":
    unittest.main()
