from textnode import text_node_to_html_node
from nodesplit import text_to_textnodes
from htmlnode import ParentNode

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_ulist = "unordered_list"
block_type_olist = "ordered_list"


def markdown_to_blocks(markdown):
    lines = markdown.split("\n\n")
    blocks = []
    for line in lines:
        if line == "":
            continue
        line = line.strip()
        blocks.append(line)
    return blocks  

def block_to_block_type(block):
    headings = ['# ',
               '## ',
               '### ',
               '#### ',
               '##### ',
               '###### '] 
    for heading in headings:
       if heading in block[:7]:
           return block_type_heading
    if block[:3] == "```" and block[-3:] == "```":
        return block_type_code
    
    quote_block = False
    unordered_block = False
    ordered_block = False
    ordered_num = 1
    block_lines = block.split("\n")
    for line in block_lines:
        if line[0] == ">":
            quote_block = True
        else:
            quote_block = False
        if line[:2] == "* " or line[:2] == "- ":
            unordered_block = True
        else:
            unordered_block = False
        if line[:3] == f"{ordered_num}. ":
            ordered_block = True
            ordered_num += 1
        else:
            ordered_block = False
    if quote_block:
        return block_type_quote
    
    if unordered_block:
        return block_type_ulist
    
    if ordered_block:
        return block_type_olist
    
    return block_type_paragraph

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        #block tag selection based on type
        match block_type:
            case "paragraph":
                block = " ".join(block.split("\n"))
                children = text_to_children(block)
                block_nodes.append(ParentNode("p", children))
            case "heading":
                if block.startswith("# "):
                    block_tag = "h1"
                if block.startswith("## "):
                    block_tag = "h2"
                if block.startswith("### "):
                    block_tag = "h3"
                if block.startswith("#### "):
                    block_tag = "h4"
                if block.startswith("##### "):
                    block_tag = "h5"
                if block.startswith("###### "):
                    block_tag = "h6"
                spacing = int(block_tag[1]) + 1
                children = text_to_children(block[spacing:])
                block_nodes.append(ParentNode(block_tag, children))
            case "quote":
                lines = block.split("\n")
                new_lines = []
                for line in lines:
                    new_lines.append(line.strip("> "))
                block = " ".join(new_lines)     
                children = text_to_children(block)
                block_nodes.append(ParentNode("blockquote", children))
            case "code":
                children = text_to_children(block[3:-3])
                pre_node = ParentNode("pre", children)
                block_nodes.append(ParentNode("code", [pre_node]))
            case "ordered_list":
                lines = block.split("\n")
                line_nodes = []
                for line in lines:
                    children = text_to_children(line[3:])
                    line_nodes.append(ParentNode("li", children))
                block_nodes.append(ParentNode("ol", line_nodes))
            case "unordered_list":
                lines = block.split("\n")
                line_nodes = []
                for line in lines:
                    children = text_to_children(line[2:])
                    line_nodes.append(ParentNode("li", children))
                block_nodes.append(ParentNode("ul", line_nodes))
    output_node = ParentNode("div", block_nodes)
    return output_node
        #create children and assemble the parent node
        

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))

    return html_nodes

def extract_title(markdown):
    lines = markdown.split("\n")
    title = ""
    for line in lines:
        if line.startswith("# "):
            title = line.strip("# ").strip()
            return title
    raise Exception("No Title Found")