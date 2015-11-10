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

# from dulwich.repo import Repo
# from dulwich.client import get_transport_and_path
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

from github import Github

g = Github("tehalexf", "PowerPoint2007")

for i in  g.get_user().get_repos():
    print i.name, i.name =='axis'
    if i.name == 'axis':
        repos = i
    print i.clone_url

print repos.name
print repos.get_commits()[0].sha



repo_path = 'data'
repo_url = 'git://github.com/rhocode/axis.git'




try:
	repo = Gittle.clone(repo_url, repo_path)
except OSError:
	repo = Gittle.init(repo_path)

repo.switch_branch(b'gh-pages')

repo.pull()

# client, host_path = get_transport_and_path("https://github.com/rhocode/axis.git")
# r = Repo.init("test", mkdir=True)
# remote_refs = client.fetch(host_path, r,
#     determine_wants=r.object_store.determine_wants_all,
#     progress=sys.stdout.write)

# branches = client.fetch(host_path, r)

# r["HEAD"] = remote_refs["HEAD"]
  