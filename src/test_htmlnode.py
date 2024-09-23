import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node,node2)

    def test_eq1(self):
        node = HTMLNode("a", "b", "c", "d")
        node2 = HTMLNode(value= "b", tag = "a", props="d", children="c")
        self.assertEqual(node,node2)

    def test_props(self):
        props1 = {"href":"https://www.google.com", "target": "_blank"}
        node = HTMLNode(props=props1)
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
