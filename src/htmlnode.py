class HTMLNode:
    def __init__(self, tag: str = None,
                value: str = None,
                children: list[object] = None,
                props: dict[str, str] = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> None:
        raise NotImplementedError

    def props_to_html(self) -> str:
        prop_str = ''
        for key, value in self.props:
            prop_str += f' {key}="{value}"'
        return prop_str

    def __repr__(self) -> str:
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'
