#!/usr/bin/env python
from sys import argv, exit
import re

def filestr(path:str) -> str:
    try:
        with open(path, 'r') as f:
            fstr = f.read()
    except FileNotFoundError:
        print(f'mkmenu: no such file or directory: \'{path}\'')
        exit(1)

    return fstr+'\n'

def rmws(txt:str):
    s = txt
    leadingws = re.compile(r'^\s+')
    blankline = re.compile(r'^\s*$')

    s = leadingws.sub('', s)
    s = blankline.sub('', s)

    return s

def linedepth(line:str) -> int:
    depth = 0
    for char in line:
        if char == ' ':
            depth += 1
        else:
            break
    
    return depth // 2

def parseitem(line:str):
    item = {
        'label':'',
        'exec':'',
        'depth':linedepth(line)
    }
    l = len(line)
    i = 0
    while i < l:
        if line[i] == ':':
            i += 1
            while i < l:
                item['exec'] += line[i]
                i += 1
            break
        else:
            item['label'] += line[i]
        i += 1
    
    item['label'] = rmws(item['label'])

    if item['label'] == '':
        return

    return item

def mkxml(menu) -> str:
    xml = '<?xml version="1.0" encoding="UTF-8">\n<openbox_menu xmlns="http://openbox.org/3.4/menu">\n'

    xml += '</openbox_menu>\n'
    return

def usage():
    print('USAGE: mkmenu [MENUFILE]')

def main(argc:int, argv:list):
    if argc < 2:
        usage()
        exit(1)

    fbuffer = filestr(argv[1])
    fbuffer = fbuffer.split('\n')
    for l in fbuffer:
        print(parseitem(l))
    
    

if __name__ == '__main__':
    argc = len(argv)
    main(argc, argv)
