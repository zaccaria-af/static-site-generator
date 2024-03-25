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


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.paragraph:
        return paragraph_to_html_node(block)
    if block_type == BlockType.heading:
        return heading_to_html_node(block)
    if block_type == BlockType.code:
        return code_to_html_node(block)
    if block_type == BlockType.ordered_list:
        return olist_to_html_node(block)
    if block_type == BlockType.unordered_list:
        return ulist_to_html_node(block)
    if block_type == BlockType.quote:
        return quote_to_html_node(block)
    raise ValueError("Invalid block type")


def markdown_to_blocks(markdown: str) -> list[str]:
    return list(filter(lambda x: x != '', list(map(lambda x: re.sub(r'\n\s*', '\n', x.strip()), markdown.split('\n\n')))))


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
    return ParentNode('p', text_to_children(' '.join(block.split('\n'))))


def heading_to_html_node(block: str) -> ParentNode:
    level = len(list(filter(lambda x: x == '#', block)))
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f'h{level}', children)


def code_to_html_node(block: str):
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)