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

def expandtermcmd(txt:str, termcmd:str) -> str:
	termre = re.compile(r':\s*@T')
	exptxt = txt
	exptxt = termre.sub(f':{termcmd} ', exptxt)

	return exptxt

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
	xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'+
		   '<openbox_menu xmlns="http://openbox.org/3.4/menu">\n'+
		   '<menu id="root-menu" label="Openbox 3">\n')

	obsubmenu = ('<!-- OpenBox Actions Menu -->\n'+
				 '<menu id="openbox" label="Openbox">\n'+
				 '<item label="Configuration Manager">\n'+
				 '<action name="Execute">\n'+
				 '<command>obconf</command>\n'+
				 '<startupnotify><enabled>yes</enabled></startupnotify>\n'+
				 '</action>\n'+
				 '</item>\n'+
				 '<item label="Reconfigure">\n'+
				 '<action name="Execute">\n'+
				 '<command>openbox --reconfigure</command>\n'+
				 '<startupnotify><enabled>yes</enabled></startupnotify>\n'+
				 '</action>\n'+
				 '</item>\n'+
				 '<item label="Restart">\n'+
				 '<action name="Execute">\n'+
				 '<command>openbox --restart</command>\n'+
				 '<startupnotify><enabled>yes</enabled></startupnotify>\n'+
				 '</action>\n'+
				 '</item>\n'+
				 '<separator />\n'+
				 '<item label="Exit">\n'+
				 '<action name="Exit"><prompt>yes</prompt></action>'
				 '</item>'
				 '</menu>\n<!-- === -->\n')

	curdepth = 0
	prevdepth = 0

	for item in menu:
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
			xml += f'<item label="{item["label"]}">\n<action name="Execute"><command>{item["exec"]}</command>\n</action>\n</item>\n'

	# Make sure the last menu is fully closed
	if curdepth > 0: xml += curdepth*'</menu>\n'

	if obitems: xml += obsubmenu

	xml += '</menu>\n</openbox_menu>\n'
	return xml

def usage():
	print("USAGE: mkmenu [-h --] [-o OUTFILE] [FILES]\n",
	"\t-h\tdisplay this help message\n",
	"\t-o\toutput file, stdout is used by default\n",
	"\t-t\tterminal command to be used (enclosed by quotes)\n",
	"\t-O\tdon't include built-in openbox menu\n",
	"\t--\tstop parsing options after '--'")

def main(argc:int, argv:list):
	if argc < 2:
		usage()
		exit(1)

	termcmd = 'st -e'
	outfile = None
	flist = []

	opts = ['-h', '-o', '-t', '-O', '--']
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
			elif argv[i] == '-t':
				try:
					i += 1
					termcmd = argv[i]
				except IndexError:
					print('mkmenu: terminal command not specified')
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
		fbuffer += filestr(f).replace('\t', '  ') # Support tabs too.
	fbuffer = expandtermcmd(fbuffer, termcmd)
	fbuffer = fbuffer.split('\n')
	menu = []
	for l in fbuffer:
		menu.append(parseitem(l))

	menu = list(filter(lambda n : n != None, menu))

	if outfile == None:
		print(mkxml(menu, obitems=includeobitems))
	else:
		with open(outfile, 'w') as f:
			f.write(mkxml(menu, obitems=includeobitems))

if __name__ == '__main__':
	argc = len(argv)
	main(argc, argv)

