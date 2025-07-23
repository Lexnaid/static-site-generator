from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent nodes must have a tag")
        
        if self.children is None:
            raise ValueError("Parent nodes must have children")
        
        # Build opening tag
        opening_tag = f"<{self.tag}"
        
        # Add properties if they exist
        if self.props:
            for key, val in self.props.items():
                opening_tag += f' {key}="{val}"'
        
        opening_tag += ">"
        
        # Build closing tag
        closing_tag = f"</{self.tag}>"
        
        # Convert children to HTML
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        
        return f"{opening_tag}{children_html}{closing_tag}"
