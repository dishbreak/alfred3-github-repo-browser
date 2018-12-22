import sys
from workflow import web, Workflow, ICON_WEB
from collections import defaultdict
import re

API_KEY = "b847ca9e4368fa1c7fb1b84e11417da6a92f9198"
API_ROOT = "https://api.github.com"
API_USER = "dishbreak"


def fetch_page(repo_url, token):
	headers = {"Authorization": "token {}".format(token)}
	response = web.get(repo_url, headers=headers)
	response.raise_for_status()
	repos = response.json()

	return repos, response.headers['Link']

def parse_header(header):
	rels = [ x.strip() for x in header.split(",")]
	links = defaultdict(lambda: '')
	for rel in rels:
		match = re.match("<(.+)>; rel=\"(.+)\"", rel)
		links[match.group(2)] = match.group(1)
	return links


def fetch_repos(api_root, token):
	repo_url = "{}/user/repos".format(API_ROOT)
	paging = True

	repos = []
	while paging:
		page, link_header = fetch_page(repo_url, token)
		repos += page
		links = parse_header(link_header)
		paging = "last" in links
		repo_url = links['next']

	return repos

def main(wf):
	query = wf.args[0] if len(wf.args) else None



	repos = wf.cached_data('repos', lambda: fetch_repos(API_ROOT, API_KEY), max_age=300)

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