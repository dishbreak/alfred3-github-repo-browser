#!/usr/bin/env python

"""
List Github Repos.

Usage:
	browse.py token API_TOKEN
	browse.py list QUERY
	browse.py list
	browse.py unset
	browse.py refresh
	browse.py timeout TIMEOUT

Commands:
	token - configure a Personal Access Token
	list - show repos using the configrued token
	unset - remove configured 
	refresh - flush cache and pick up new repos
	timeout - set timeout for cache in seconds

"""
import sys
from deps.workflow import Workflow3, ICON_WEB, PasswordNotFound
from deps.workflow.notify import notify
from deps.docopt import docopt
from github import fetch_repos
from constants import KEYCHAIN_GITHUB_TOKEN, API_ROOT, REPO_CACHE

UPDATE_PROCESS = "update"

def parse_args(args):
	"""
	Convenience wrapper for call to Docopt
	"""
	return docopt(__doc__, args)

def get_repos(api_key, timeout=0):
	"""
	Load repos from cache. If the cache is empty, use the embedded Github library
	to fetch the needed data.

	Parameters:
	- api_token: A github API token
	"""
	return wf.cached_data(REPO_CACHE, lambda: fetch_repos(API_ROOT, api_key), max_age=timeout)

def main(wf):
	args = parse_args(wf.args)

	if "repos" not in wf.settings:
		wf.settings["repos"] = { "timeout": 3600 }
		wf.settings.save()

	wf.logger.info("Timeout is '{}'".format(wf.settings['repos']['timeout']))
	if args['token']:
		wf.save_password(KEYCHAIN_GITHUB_TOKEN, args['API_TOKEN'])
		notify("Saved API Token to Keychain", "Workflow is ready for use!")
		return 0
	if args['unset']:
		try:
			wf.delete_password(KEYCHAIN_GITHUB_TOKEN)
			notify("Removed API Token from Keychain", "Add a new token in order to use the workflow.")
		except PasswordNotFound:
			wf.logger.info("No token to delete!")
		return 0
	if args['timeout']:
		try:
			timeout = int(args['TIMEOUT'])
			wf.settings['repos']['timeout'] = timeout
			wf.settings.save()
			notify("Timeout Set", "Accepted new value of '{}'".format(timeout))
		except ValueError:
			raise Exception("Got non-numeric input '{}'".format(args['TIMEOUT']))
		return 0

	try:
		api_key = wf.get_password(KEYCHAIN_GITHUB_TOKEN)
	except PasswordNotFound:
		raise Exception("Missing Github token, set using 'githubsettings' keyword.")

	if args['refresh']:
		wf.clear_cache(lambda name: name == "{}.cpickle".format(REPO_CACHE))
		notify("Reindexing Github Repos", "I'll let you know once I've cleaned things up.")
		get_repos(api_key)
		notify("Reindexing Github Repos Complete", "Good to go!")


	query = args['QUERY'] if 'QUERY' in args else None

	repos = get_repos(api_key, wf.settings['repos']['timeout'])

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
	wf = Workflow3()
	sys.exit(wf.run(main))