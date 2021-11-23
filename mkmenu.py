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

def usage():
    print(  'USAGE: mkmenu [MENUFILE]')

def main(argc:int, argv:list):
    if argc < 2:
        usage()
        exit(1)
    loadfile(argv[1])

if __name__ == '__main__':
    argc = len(argv)
    main(argc, argv)
