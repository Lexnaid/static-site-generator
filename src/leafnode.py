from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        
        # Generate the opening tag with properties
        opening_tag = f"<{self.tag}"

        if self.props:
            for key, value in self.props.items():
                opening_tag += f' {key}="{value}"'

        opening_tag += ">"


        closing_tag = f"</{self.tag}>"

        return f"{opening_tag}{self.value}{closing_tag}"

