import os
import shutil
from blocks import markdown_to_html_node, extract_title
from htmlnode import HTMLNode
from pathlib import Path

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    f = open(from_path)
    from_file = f.read()
    f.close()

    t = open(template_path)
    template = t.read()
    t.close()

    html = markdown_to_html_node(from_file).to_html()

    title = extract_title(from_file)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    o = open(dest_path, 'w')
    o.write(template)
    o.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):

    for filename in os.listdir(dir_path_content):
        content_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(content_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(content_path, template_path, dest_path)
        else:
            generate_pages_recursive(content_path, template_path, dest_path)