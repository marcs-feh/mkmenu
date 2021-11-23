#!/usr/bin/env python
from sys import argv, exit

def filestr(path:str) -> str:
    try:
        with open(path, 'r') as f:
            fstr = f.read()
    except FileNotFoundError:
        print(f'mkmenu: no such file or directory: \'{path}\'')
        exit(1)

    return fstr

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
        'name':'',
        'exec':''
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
            item['name'] += line[i]
        i += 1
    
    return item

def usage():
    print('USAGE: mkmenu [MENUFILE]')

def main(argc:int, argv:list):
    if argc < 2:
        usage()
        exit(1)

    fbuffer = filestr(argv[1])
    

if __name__ == '__main__':
    argc = len(argv)
    main(argc, argv)
