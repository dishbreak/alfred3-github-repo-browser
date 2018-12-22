import sys
from workflow import web, Workflow, ICON_WEB

API_KEY = "b847ca9e4368fa1c7fb1b84e11417da6a92f9198"
API_ROOT = "https://api.github.com"
API_USER = "dishbreak"

def main(wf):
	query = wf.args[0] if len(wf.args) else None

	repo_url = "{}/user/repos".format(API_ROOT)
	headers = {"Authorization": "token {}".format(API_KEY)}
	response = web.get(repo_url, headers=headers)
	response.raise_for_status()
	repos = response.json()

	if query:
		repos = wf.filter(query, repos, key=lambda x: x['name'])

	for repo in repos:
		# name, html_url, description, id
		wf.add_item(title=repo['name'],
			subtitle=repo['description'],
			arg=repo['html_url'],
			valid=True,
			icon=ICON_WEB)
	wf.send_feedback()

if __name__ == '__main__':
	wf = Workflow()
	sys.exit(wf.run(main))