import os
import shutil
import re
from pathlib import Path
from block_markdown import markdown_to_html_node


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
    if not os.path.exists(dir_path_content):
        raise ValueError("Invalid source directory provided. Path does not exist.")
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    for entry in os.listdir(dir_path_content):
        rel_path = os.path.join(dir_path_content, entry)
        if os.path.isfile(rel_path):
            generate_page(rel_path, template_path, os.path.join(dest_dir_path, entry))
        else:
            generate_pages_recursive(rel_path, template_path, os.path.join(dest_dir_path, entry))


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    if not os.path.exists(from_path):
        raise ValueError("Invalid source directory provided. Path does not exist.")
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    with open(from_path) as f:
        content = f.read()
        f.close()
    with open(template_path) as f:
        template = f.read()
        f.close()
    html_content = markdown_to_html_node(content)
    title = extract_title(content)
    template = template.replace('{{ Content }}', html_content.to_html()).replace('{{ Title }}', title)
    full_html = open(dest_path, 'w')
    full_html.write(template)
    md_path = Path(dest_path)
    md_path.rename(md_path.with_suffix('.html'))
    full_html.close()


def extract_title(markdown: str) -> str:
    pattern = r'^#{1}\s+\S.*'
    match = re.findall(pattern, markdown)
    if len(match) != 1:
        raise ValueError("Invalid markdown. All pages need a single h1 header.")
    return match[0]


def copy_dir(source_dir: str, dest_dir: str) -> None:
    if not os.path.exists(source_dir):
        raise ValueError("Invalid source directory provided. Path does not exist.")
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.mkdir(dest_dir)
    for entry in os.listdir(source_dir):
        rel_path = os.path.join(source_dir, entry)
        if os.path.isfile(rel_path):
            shutil.copy(rel_path, dest_dir)
        else:
            copy_dir(rel_path, os.path.join(dest_dir, entry))


def main():
    copy_dir('static', 'public')
    generate_pages_recursive('content', 'template.html', 'public')


if __name__ == "__main__":
    main()
