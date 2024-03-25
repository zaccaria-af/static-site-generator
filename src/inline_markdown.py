import re
from src.textnode import TextNode, TextType


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.text)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.bold)
    nodes = split_nodes_delimiter(nodes, "*", TextType.italic)
    nodes = split_nodes_delimiter(nodes, "`", TextType.code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    split_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.text:
            split_nodes.append(node)
            continue
        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown: Opening delimiter not closed.")
        for i in range(len(sections)):
            if sections[i] == '':
                continue
            if i % 2 != 0:
                split_nodes.append(TextNode(sections[i], text_type))
            else:
                split_nodes.append(TextNode(sections[i], TextType.text))
    return split_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    split_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.text:
            split_nodes.append(node)
            continue
        old_text = node.text
        extracted_images = extract_markdown_images(old_text)
        if len(extracted_images) == 0:
            split_nodes.append(node)
            continue
        for image in extracted_images:
            split_text = old_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(split_text) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if split_text[0] != '':
                split_nodes.append(TextNode(split_text[0], TextType.text))
            split_nodes.append(TextNode(image[0], TextType.image, image[1]))
            old_text = split_text[1]
        if old_text != '':
            split_nodes.append(TextNode(old_text, TextType.text))
    return split_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    split_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.text:
            split_nodes.append(node)
            continue
        old_text = node.text
        extracted_links = extract_markdown_links(old_text)
        if len(extracted_links) == 0:
            split_nodes.append(node)
            continue
        for link in extracted_links:
            split_text = old_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(split_text) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if split_text[0] != '':
                split_nodes.append(TextNode(split_text[0], TextType.text))
            split_nodes.append(TextNode(link[0], TextType.link, link[1]))
            old_text = split_text[1]
        if old_text != '':
            split_nodes.append(TextNode(old_text, TextType.text))
    return split_nodes


def extract_markdown_images(text: str) -> list[tuple]:
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text: str) -> list[tuple]:
    pattern = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches
