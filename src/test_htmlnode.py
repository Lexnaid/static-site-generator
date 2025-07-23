from htmlnode import *

def test_htmlnode():
    # Test case 1: Basic HTMLNode with tag and value
    node1 = HTMLNode(tag="p", value="This is a paragraph.")
    assert node1.tag == "p"
    assert node1.value == "This is a paragraph."
    assert node1.children is None
    assert node1.props is None
    assert node1.props_to_html() == ''
    
    # Test case 2: HTMLNode with children and props
    child_node = HTMLNode(tag="span", value="This is a span.")
    node2 = HTMLNode(tag="div", children=[child_node], props={"class": "container"})
    assert node2.tag == "div"
    assert node2.value is None
    assert len(node2.children) == 1
    assert node2.children[0].tag == "span"
    assert node2.props == {"class": "container"}
    assert node2.props_to_html() == 'class="container"'
    
    # Test case 3: HTMLNode without tag, but with value
    node3 = HTMLNode(value="Just some text.")
    assert node3.tag is None
    assert node3.value == "Just some text."
    assert node3.children is None
    assert node3.props is None
    assert node3.props_to_html() == ''
    # Test case 4: HTMLNode with no value and no children
    node4 = HTMLNode(tag="br")
    assert node4.tag == "br"
    assert node4.value is None
    assert node4.children is None
    assert node4.props is None
    assert node4.props_to_html() == ''

    # Test case 5: HTMLNode with props only
    node5 = HTMLNode(tag="a", props={"href": "https://example.com", "target": "_blank"})
    assert node5.tag == "a"
    assert node5.value is None
    assert node5.children is None
    assert node5.props == {"href": "https://example.com", "target": "_blank"}
    assert node5.props_to_html() == 'href="https://example.com" target="_blank"'
    

if __name__ == "__main__":
    test_htmlnode()
    print("All tests passed!")
# This is a simple test suite for the HTMLNode class
# It checks the basic functionality of the class and its methods
