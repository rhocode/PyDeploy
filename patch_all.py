import os
liblocation = os.path.dirname(os.path.abspath(__file__)) + '/lib'
tempmkdir = os.mkdir

def modifiedMake(name, mode=False):
	try:
		if (mode):
			tempmkdir(name, mode)
		else:
			tempmkdir(name)
	except OSError:
		pass

os.mkdir = modifiedMake

import sys
sys.path.append(liblocation)
sys.path.append(liblocation + '/github')

from gittle import Gittle

import fnmatch
import posixpath
import re
import functools

def translate(pat):
    pat = list(pat)
    i, n = 0, len(pat)
    res = ''
    while i < n:
        c = pat[i]
        i = i+1
        if c == '*':
            res = res + '.*'
        elif c == '?':
            res = res + '.'
        elif c == '[':
            j = i
            if j < n and pat[j] == '!':
                j = j+1
            if j < n and pat[j] == ']':
                j = j+1
            while j < n and pat[j] != ']':
                j = j+1
            if j >= n:
                res = res + '\\['
            else:
                stuff = pat[i:j].replace('\\','\\\\')
                i = j+1
                if stuff[0] == '!':
                    stuff = '^' + stuff[1:]
                elif stuff[0] == '^':
                    stuff = '\\' + stuff
                res = '%s[%s]' % (res, stuff)
        else:
            res = res + re.escape(c)
    return res + '\Z(?ms)'

fnmatch.translate = translate