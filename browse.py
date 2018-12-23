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
from workflow import Workflow, ICON_WEB, PasswordNotFound
from workflow.notify import notify
from docopt import docopt
from github import fetch_repos

API_ROOT = "https://api.github.com"

__KEYCHAIN_GITHUB_TOKEN = "github_token"

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
		except PasswordNotFound:
			wf.logger.info("No token to delete!")
		return 0

	try:
		api_key = wf.get_password(__KEYCHAIN_GITHUB_TOKEN)
	except PasswordNotFound:
		raise Exception('Missing Github token, set with githubtoken')


	query = args['QUERY'] if 'QUERY' in args else None

	repos = wf.cached_data('repos', lambda: fetch_repos(API_ROOT, api_key), max_age=300)

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