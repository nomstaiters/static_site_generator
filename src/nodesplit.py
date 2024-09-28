import re
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == text_type_text:
            delimited_list = node.text.split(delimiter)
            if len(delimited_list) % 2 == 0:
                raise Exception(f"Invalid Delimiter syntax: no closing delimiter: {delimiter}")
            for i in range(len(delimited_list)):
                if i % 2 == 0:
                    if delimited_list[i] == '':
                        pass
                    else:
                        new_nodes.append(TextNode(delimited_list[i], text_type_text))
                else:
                    new_nodes.append(TextNode(delimited_list[i], text_type)) 
        else:
            new_nodes.append(node)
    return new_nodes    

def extract_markdown_images(text):
    
    output = re.findall(r"\!\[(.*?)\]\((.*?)\)",text)
    
    return output

def extract_markdown_links(text):

    output = re.findall(r"\[(.*?)\]\((.*?)\)",text)

    return output

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == text_type_text:
            split_list = re.split(r"\!\[.*?\]\(.*?\)", node.text)
            images = extract_markdown_images(node.text)
            if len(images) == 0:
                new_nodes.append(node)
                continue
            for i in range(len(split_list)):
                if split_list[i] == '' and len(images) > i:
                    new_nodes.append(TextNode(images[i][0], text_type_image, images[i][1]))
                elif split_list[i] != '' and len(images) > i:
                    new_nodes.append(TextNode(split_list[i], text_type_text))
                    new_nodes.append(TextNode(images[i][0], text_type_image, images[i][1]))
                elif split_list[i] != '':
                    new_nodes.append(TextNode(split_list[i], text_type_text))
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == text_type_text:
            split_list = re.split(r"\[.*?\]\(.*?\)", node.text)
            images = extract_markdown_links(node.text)
            if len(images) == 0:
                new_nodes.append(node)
                continue
            for i in range(len(split_list)):
                if split_list[i] == '' and len(images) > i:
                    new_nodes.append(TextNode(images[i][0], text_type_link, images[i][1]))
                elif split_list[i] != '' and len(images) > i:
                    new_nodes.append(TextNode(split_list[i], text_type_text))
                    new_nodes.append(TextNode(images[i][0], text_type_link, images[i][1]))
                elif split_list[i] != '':
                    new_nodes.append(TextNode(split_list[i], text_type_text))
        else:
            new_nodes.append(node)
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    bold_nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    italic_nodes = split_nodes_delimiter(bold_nodes, "*", text_type_italic)
    code_nodes = split_nodes_delimiter(italic_nodes, "`", text_type_code)
    return split_nodes_link(split_nodes_image(code_nodes))
    