import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node", text_type_text)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is a text node", text_type_italic)
        self.assertNotEqual(node, node2)

    def test_neq2(self):
        node = TextNode("This is a text node", text_type_code)
        node2 = TextNode("This is a text node2", text_type_code)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", text_type_link, None)
        node2 = TextNode("This is a text node", text_type_link)
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", text_type_image, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, image, https://www.boot.dev)", repr(node)
        )

if __name__ == "__main__":
    unittest.main()
