class HTMLNode:
    def __init__(self, tag: str = None,
                 value: str = None,
                 children: list[object] = None,
                 props: dict[str, str] = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self) -> str:
        if self.props is None:
            return ''
        return ''.join(map(lambda kv: f' {kv[0]}="{kv[1]}"', self.props.items()))

    def __repr__(self) -> str:
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'


class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict[str, str] = None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[object], props: dict[str, str] = None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("Invalid HTML: no tag")
        if self.children is None:
            raise ValueError("Invalid ParentNode: no children")
        html_content = ''.join(list(map(lambda child: child.to_html(), self.children)))
        return f'<{self.tag}{self.props_to_html()}>{html_content}</{self.tag}>'
