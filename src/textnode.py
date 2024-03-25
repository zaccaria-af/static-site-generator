from enum import Enum
from src.htmlnode import LeafNode


class TextType(Enum):
    text = "text"
    bold = "bold"
    italic = "italic"
    code = "code"
    link = "link"
    image = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: object) -> bool:
        return all(
            getattr(self, attr) == getattr(other, attr) for attr in ['text', 'text_type', 'url']
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

    def text_node_to_html_node(self) -> LeafNode:
        match self.text_type:
            case TextType.text:
                return LeafNode(value=self.text)
            case TextType.bold:
                return LeafNode(tag='b', value=self.text)
            case TextType.italic:
                return LeafNode(tag='i', value=self.text)
            case TextType.code:
                return LeafNode(tag='code', value=self.text)
            case TextType.link:
                return LeafNode(tag='a', value=self.text, props={'href': self.url})
            case TextType.image:
                return LeafNode(tag='img', value='', props={'src': self.url, 'alt': self.text})
            case _:
                raise ValueError(f"Invalid text type: {self.text_type}")


