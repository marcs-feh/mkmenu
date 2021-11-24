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
    headtailws = re.compile(r'(^\s+|\s+$)')
    blankline = re.compile(r'^\s*$')

    s = headtailws.sub('', s)
    s = blankline.sub('', s)

    return s

def tidylabel(label:str) -> str:
    properlabel = label.lower()
    ws = re.compile(r'\s+')
    properlabel = ws.sub('-', properlabel)
    return properlabel

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
    item['exec'] = rmws(item['exec'])

    if item['label'] == '': return

    if item['exec'] == '': item['exec'] = None

    return item

def mkxml(menu:list, obitems=True) -> str:
    xml = '<?xml version="1.0" encoding="UTF-8">\n<openbox_menu xmlns="http://openbox.org/3.4/menu">\n<menu id="root-menu" label="Openbox 3"?>\n'
    obsubmenu = '<!-- OpenBox Menu (automatically generated) -->\n<menu id="openbox" label="Openbox" ><item label="Configuration Manager"><action name="Execute"><command>obconf</command><startupnotify><enabled>yes</enabled></startupnotify></action></item><item label="Reconfigure"><action name="Execute"><command>openbox --reconfigure</command><startupnotify><enabled>yes</enabled></startupnotify></action></item><item label="Restart"><action name="Execute"><command>openbox --restart</command><startupnotify><enabled>yes</enabled></startupnotify></action></item><separator /><item label="Exit"><action name="Execute"><command>openbox --exit</command><startupnotify><enabled>yes</enabled></startupnotify></action></item></menu>\n<!-- -->\n'
    curdepth = 0
    prevdepth = 0

    for i, item in enumerate(menu):
        prevdepth = curdepth
        curdepth = item['depth']

        if curdepth < prevdepth:
            diff = prevdepth - curdepth
            xml += diff*'</menu>\n'

        if item['exec'] == None:
            if item['label'] == '---':
                xml += '<separator />\n'
            elif item['label'][0] == '#':
                xml += f'<separator label="{(item["label"])[1:]}"/>\n'
            else:
                xml += f'<menu id="{tidylabel(item["label"])}" label="{item["label"]}">\n'

        else:
            xml += f'<item label="{item["label"]}">\n<action name="Execute"><command>{item["exec"]}</command>\n'
            xml += '<startupnotify><enabled>yes</enabled></startupnotify>\n</action>\n</item>\n'

    if obitems:
        xml += obsubmenu
    xml += '</menu>\n</openbox_menu>\n'
    return xml

def usage():
    print(  'USAGE: mkmenu [-h --] [-o OUTFILE] [FILES]\n',
            '    -h    display this help message\n',
            '    -o    output file, stdout is used by default\n',
            '    -O    don\'t include built-in openbox menu\n',
            '    --    stop parsing options after \'--\'')

def main(argc:int, argv:list):
    if argc < 2:
        usage()
        exit(1)

    outfile = None
    flist = []

    opts = ['-h', '-o', '-O','--']
    includeobitems = True

    i = 1
    while i < argc:
        if argv[i] in opts:
            if argv[i] == '--':
                opts = []
            elif argv[i] == '-h':
                usage()
                exit(0)
            elif argv[i] == '-o':
                try:
                    i += 1
                    outfile = argv[i]
                except IndexError:
                    print('mkmenu: no output file provided.')
                    exit(1)
            elif argv[i] == '-O':
                includeobitems = False
        else:
            flist.append(argv[i])
        i += 1
    
    if len(flist) == 0:
        usage()
        exit(1)

    fbuffer = ''
    for f in flist:
        fbuffer += filestr(f)

    fbuffer = fbuffer.split('\n')
    menu = []
    for l in fbuffer:
        menu.append(parseitem(l))

    menu = list(filter(lambda n : n != None, menu))

    if outfile == None:
        print(mkxml(menu))
    else:
        with open(outfile, 'w') as f:
            f.write(mkxml(menu, obitems=includeobitems))
    
if __name__ == '__main__':
    argc = len(argv)
    main(argc, argv)
