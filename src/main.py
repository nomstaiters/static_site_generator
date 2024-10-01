from textnode import TextNode
from htmlnode import HTMLNode, ParentNode, LeafNode
import os
import shutil

from copystatic import copy_files_recursive
from page_generator import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
template_path = "template.html"
dest_path = "./public"
content_path = "./content"

def main():
    print("Deleting Public Directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory")
    copy_files_recursive(dir_path_static, dir_path_public)

    generate_pages_recursive(content_path, template_path, dest_path)





if __name__ == "__main__":
    main()