import unittest
from src.textnode import TextNode, TextType
from src.inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_link,
    split_nodes_image
)


class TextInlineMarkdown(unittest.TestCase):
    def test_split_nodes_italic(self):
        old_nodes = [TextNode("This is some *italic* text", TextType.text)]
        delimited_nodes = split_nodes_delimiter(old_nodes, '*', TextType.italic)
        expected_delimited_nodes = [
            TextNode("This is some ", TextType.text),
            TextNode("italic", TextType.italic),
            TextNode(" text", TextType.text)
        ]
        self.assertEqual(delimited_nodes, expected_delimited_nodes)

    def test_split_nodes_bold(self):
        old_nodes = [TextNode("This is some **bold** text", TextType.text)]
        delimited_nodes = split_nodes_delimiter(old_nodes, '**', TextType.bold)
        expected_delimited_nodes = [
            TextNode("This is some ", TextType.text),
            TextNode("bold", TextType.bold),
            TextNode(" text", TextType.text)
        ]
        self.assertEqual(delimited_nodes, expected_delimited_nodes)

    def test_split_nodes_code(self):
        old_nodes = [TextNode("This is some `code` text", TextType.text)]
        delimited_nodes = split_nodes_delimiter(old_nodes, '`', TextType.code)
        expected_delimited_nodes = [
            TextNode("This is some ", TextType.text),
            TextNode("code", TextType.code),
            TextNode(" text", TextType.text)
        ]
        self.assertEqual(delimited_nodes, expected_delimited_nodes)

    def test_split_nodes_multiple(self):
        old_nodes = [
            TextNode("This is some **bold text**", TextType.text),
            TextNode("**bold** is this text", TextType.text),
            TextNode("**bold**", TextType.text)
        ]
        delimited_nodes = split_nodes_delimiter(old_nodes, '**', TextType.bold)
        expected_delimited_nodes = [
            TextNode("This is some ", TextType.text),
            TextNode("bold text", TextType.bold),
            TextNode("bold", TextType.bold),
            TextNode(" is this text", TextType.text),
            TextNode("bold", TextType.bold),
        ]
        self.assertEqual(delimited_nodes, expected_delimited_nodes)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.text),
                TextNode("image", TextType.image, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.com/image.png)",
            TextType.text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.image, "https://www.example.com/image.png"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.text),
                TextNode("image", TextType.image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.text),
                TextNode(
                    "second image", TextType.image, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.text,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.text),
                TextNode("link", TextType.link, "https://boot.dev"),
                TextNode(" and ", TextType.text),
                TextNode("another link", TextType.link, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.text),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
