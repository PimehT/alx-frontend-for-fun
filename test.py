#!/usr/bin/python3
import re


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


def ordered_list(lines):
    modified_lines = []
    check_ol = False
    check_ul = False

    for k, v in enumerate(lines):
        if v.startswith('* '):
            v = v.replace('* ', '<li>')
            if v.endswith('\n'):
                v = v[:-1] + '</li>'
            v += '\n'
            if not check_ol:
                modified_lines.append('<ol>\n')
                check_ol = True
        elif v.startswith('- '):
            v = v.replace('- ', '<li>')
            if v.endswith('\n'):
                v = v[:-1] + '</li>'
            v += '\n'
            if not check_ul:
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

    return modified_list

def bold_or_emphasis(lines):
    modified_lines = []
    for line in lines:
        line = re.sub(r'\*\*(\S.*?)\*\*', r'<b>\1</b>', line)
        line = re.sub(r'__(\S.*?)__', r'<em>\1</em>', line)
        modified_lines.append(line)
    return modified_lines


with open("t.txt", 'r') as f:
    lines = f.readlines()
    lines = h_level(lines)
    lines = ordered_list(lines)
    lines = paragraph(lines)
    lines = bold_or_emphasis(lines)

with open('output.html', 'w') as o:
    o.writelines(lines)
