import re
from enum import Enum
from src.htmlnode import ParentNode
from src.inline_markdown import text_to_textnodes
from src.textnode import TextNode


class BlockType(Enum):
    paragraph = "paragraph",
    heading = "heading",
    code = "code",
    quote = "quote",
    unordered_list = "unordered_list",
    ordered_list = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    return list(map(lambda x: re.sub(r'\n\s*', '\n', x.strip()),
                    list(filter(lambda x: x != '', markdown.split('\n\n')))))


def block_to_block_type(block: str) -> BlockType:
    block_pattern = {
        r'^#{1,6}\s+\S.*': BlockType.heading,
        r'\`\`(?:[\s\S]*?)\`\`': BlockType.code,
        r'((^(\>{1})(\s)(.*)(?:$)?)+)': BlockType.quote,
        r'(^(\W{1})(\s)(.*)(?:$)?)+': BlockType.unordered_list,
        r'(^(\d+\.)(\s)(.*)(?:$)?)+': BlockType.ordered_list
    }

    for pattern, block_type in block_pattern.items():
        if re.match(pattern, block):
            return block_type
    return BlockType.paragraph


def text_to_children(text: str) -> list[TextNode]:
    return list(map(lambda x: x.text_node_to_html_node(), text_to_textnodes(text)))


def paragraph_to_html_node(block: str) -> ParentNode:
    return ParentNode('p', list(map(lambda x: text_to_children(x), ' '.join(block.split('\n')))))
