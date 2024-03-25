import unittest

from src.textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.text)
        node2 = TextNode("This is a text node", TextType.text)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.bold)
        node2 = TextNode("This is a text node", TextType.italic)
        self.assertNotEqual(node, node2)

    def test_neq2(self):
        node = TextNode("This is a text node", TextType.code)
        node2 = TextNode("This is a text node2", TextType.code)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.link, None)
        node2 = TextNode("This is a text node", TextType.link)
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.image, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, image, https://www.boot.dev)", repr(node)
        )


if __name__ == "__main__":
    unittest.main()
