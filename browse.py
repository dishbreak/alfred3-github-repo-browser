#!/usr/bin/env python

"""
List Github Repos.

Usage:
	browse.py token API_TOKEN
	browse.py list QUERY
	browse.py list
	browse.py clean

Commands:
	token - configure a Personal Access Token
	list - show repos using the configrued token
	clean - remove configured 

"""
import sys
from workflow import web, Workflow, ICON_WEB, PasswordNotFound
from workflow.notify import notify
from collections import defaultdict
from docopt import docopt
import re

API_KEY = "b847ca9e4368fa1c7fb1b84e11417da6a92f9198"
API_ROOT = "https://api.github.com"
API_USER = "dishbreak"
PAGE_SIZE = 100

__KEYCHAIN_GITHUB_TOKEN = "github_token"

def fetch_page(repo_url, token, page_size):
	headers = {"Authorization": "token {}".format(token)}
	params = {"per_page": 100}
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


def fetch_repos(api_root, token, page_size):
	repo_url = "{}/user/repos".format(api_root)
	paging = True

	repos = []
	while paging:
		page, link_header = fetch_page(repo_url, token, page_size)
		repos += page
		links = parse_header(link_header)
		paging = "last" in links
		repo_url = links['next']

	return repos

def parse_args(args):
	return docopt(__doc__, args)

def main(wf):
	args = parse_args(wf.args)

	if args['token']:
		wf.save_password(__KEYCHAIN_GITHUB_TOKEN, args['API_TOKEN'])
		notify("Saved API Token to Keychain", "Use 'githubclean' to remove.")
		return 0
	if args['clean']:
		try:
			wf.delete_password(__KEYCHAIN_GITHUB_TOKEN)
			notify("Removed API Token from Keychain", "Use 'githubtoken' to add a new token.")
		except PasswordNotFound as e:
			wf.logger.info("No token to delete!")
		return 0

	try:
		api_key = wf.get_password(__KEYCHAIN_GITHUB_TOKEN)
	except PasswordNotFound as e:
		raise Exception('Missing Github token, set with githubtoken')


	query = args['QUERY'] if 'QUERY' in args else None

	repos = wf.cached_data('repos', lambda: fetch_repos(API_ROOT, api_key, PAGE_SIZE), max_age=300)

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