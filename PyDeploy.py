from patch_all import *
from github import Github
import threading
import time

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

LOGINS = {}
REPOS = set()

class GittleGitHubRepo:
	def __init__(self, gittle, github, last_sha):
		self.gittle = gittle
		self.github = github
		self.last_sha = last_sha

	def get_sha(self):
		return self.github.get_commits()[0].sha[0:10]

	def needs_update(self):
		return self.github.get_commits()[0].sha[0:10] != self.last_sha

	def update(self):
		self.gittle.pull()
		self.last_sha = self.github.get_commits()[0].sha[0:10] 

#store multiple logins
def login():
	f =  open("login.txt",'r')
	while(True):
		username = f.readline()
		password = f.readline()
		if not password:
			break #EOF reached
		username = username.replace('\n', '')
		if username not in LOGINS:
			LOGINS[username] = Github(username, password.replace('\n', ''))

#Fetch all git repos
def getRepos():
	f =  open("trackedrepos.txt",'r')
	tempGittleRepos = {}
	while(True):
		line = f.readline()
		if not line:
			break #EOF reached
		line = line.replace('\n', '').replace(' ','').split(',')
		if len(line) == 4:
			if line[0] not in LOGINS:
				print("You did not provide credentials for " + line[0])
			else:
				try:
					repo = Gittle.clone(line[1], line[3])
				except OSError:
					repo = Gittle.init(line[3])
				tempGittleRepos[line[1]] = repo
				repo.switch_branch(str.encode(line[2]))
		else:
			print("Invalid line: " + ' '.join(line))
	for user in LOGINS:
		myrepos = LOGINS[user].get_user().get_repos()
		for repo in myrepos:
			cloneurl = repo.clone_url.replace("api.", '')
			if cloneurl in tempGittleRepos:
				REPOS.add(GittleGitHubRepo(tempGittleRepos[cloneurl], \
					repo, repo.get_commits()[0].sha[0:10]))


login()
getRepos()



def poll():
	print("Polling")
	for i in REPOS:
		if i.needs_update():
			i.update()
			print("Updated " + i)	
	time.sleep(2)
	return

def keepPolling():
	while(True):
		poll()
		

if __name__ == "__main__":
	t = threading.Thread(target=keepPolling)
	t.start()
	app.run(host='0.0.0.0')
	

# for i in  g.get_user().get_repos():
#     print i.name, i.name =='axis'
#     if i.name == 'axis':
#         repos = i
#     print i.clone_url

# print repos.name
# print repos.get_commits()[0].sha



# repo_path = 'data'
# repo_url = 'git://github.com/rhocode/axis.git'




# try:
# 	repo = Gittle.clone(repo_url, repo_path)
# except OSError:
# 	repo = Gittle.init(repo_path)



# repo.pull()

# client, host_path = get_transport_and_path("https://github.com/rhocode/axis.git")
# r = Repo.init("test", mkdir=True)
# remote_refs = client.fetch(host_path, r,
#     determine_wants=r.object_store.determine_wants_all,
#     progress=sys.stdout.write)

# branches = client.fetch(host_path, r)

# r["HEAD"] = remote_refs["HEAD"]
  