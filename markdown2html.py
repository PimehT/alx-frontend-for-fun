#!/usr/bin/python3
""" this script takes two args:
arg1: name of markdown file
arg2: output file name
Usage: ./markdown2html.py README.md README.html
"""
import hashlib
import re
import sys


def h_level(lines):
    modified_lines = []
    for line in lines:
        pattern = r'^#+ '
        if re.match(pattern, line):
            level = len(re.match(pattern, line).group(0)) - 1
            line = re.sub(pattern, f"<h{level}>", line).rstrip()
            line += f"</h{level}>\n"
        modified_lines.append(line)
    return modified_lines


def process_list(lines):
    modified_lines = []
    check_ol = False
    check_ul = False

    for k, v in enumerate(lines):
        if v.startswith('* '):
            v = v.replace('* ', '<li>')
            if v.endswith('\n'):
                v = v[:-1] + '</li>'
            v += '\n'
            if check_ol is False:
                modified_lines.append('<ol>\n')
                check_ol = True
        elif v.startswith('- '):
            v = v.replace('- ', '<li>')
            if v.endswith('\n'):
                v = v[:-1] + '</li>'
            v += '\n'
            if check_ul is False:
                modified_lines.append('<ul>\n')
                check_ul = True
        else:
            if check_ol:
                modified_lines.append('</ol>\n')
                check_ol = False
            if check_ul:
                modified_lines.append('</ul>\n')
                check_ul = False

        modified_lines.append(v)

        if k == len(lines) - 1:
            if check_ol:
                modified_lines.append('</ol>\n')
                check_ol = False
            if check_ul:
                modified_lines.append('</ul>\n')
                check_ul = False

    return modified_lines


def paragraph(lines):
    modified_list = []
    tags = [
        '<h1>', '</h1>',
        '<h2>', '</h2>',
        '<h3>', '</h3>',
        '<h4>', '</h4>',
        '<h5>', '</h5>',
        '<h6>', '</h6>',
        '<ul>', '</ul>',
        '<ol>', '</ol>',
        '<li>', '</li>',
        '\n'
    ]

    for k, v in enumerate(lines):
        for tag in tags:
            if v.startswith(tag):
                modified_list.append(v)
                break
        else:
            if modified_list and modified_list[-1] == '<br/>\n':
                modified_list.append(v)
            else:
                modified_list.append('<p>\n')
                modified_list.append(v)

            if k != len(lines) - 1:
                for tag in tags:
                    if lines[k+1].startswith(tag):
                        modified_list.append('</p>\n')
                        break
                else:
                    modified_list.append('<br/>\n')

    if (
        modified_list and
        not modified_list[-1].endswith(('</p>\n', '</ol>\n', '</ul>\n'))
    ):
        modified_list.append('</p>\n')

    return modified_list


def bold_or_emphasis(lines):
    modified_lines = []
    for line in lines:
        line = re.sub(r'\*\*(\S.*?)\*\*', r'<b>\1</b>', line)
        line = re.sub(r'__(\S.*?)__', r'<em>\1</em>', line)

        line = re.sub(
            r'\[\[(.*?)\]\]',
            lambda match: hashlib.md5(match.group(1).encode()).hexdigest(),
            line
        )
        line = re.sub(
            r'\(\((.*?)\)\)',
            lambda match: match.group(1).replace('c', '').replace('C', ''),
            line
        )
        modified_lines.append(line)
    return modified_lines


def convert_markdown_to_html(markdown_file, output_file):
    if not markdown_file.endswith(".md") or not output_file.endswith(".html"):
        print("Usage: ./markdown2html.py README.md README.html",
              file=sys.stderr)
        sys.exit(1)

    try:
        with open(markdown_file, 'r') as f:
            lines = f.readlines()

        modified_lines = process_list(lines)
        modified_lines = h_level(modified_lines)
        modified_lines = paragraph(modified_lines)
        modified_lines = bold_or_emphasis(modified_lines)

        with open(output_file, 'w') as o:
            o.writelines(modified_lines)
    except FileNotFoundError:
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html",
              file=sys.stderr)
        sys.exit(1)

    markdown_file = sys.argv[1]
    output_file = sys.argv[2]
    convert_markdown_to_html(markdown_file, output_file)
