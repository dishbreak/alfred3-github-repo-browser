from workflow import web
from collections import defaultdict
import re

PAGE_SIZE = 100

def fetch_page(repo_url, token, page_size):
	headers = {"Authorization": "token {}".format(token)}
	params = {"per_page": page_size}
	response = web.get(repo_url, params, headers=headers)
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
	repo_url = "{}/user/repos".format(api_root)
	paging = True

	repos = []
	while paging:
		page, link_header = fetch_page(repo_url, token, PAGE_SIZE)
		repos += page
		links = parse_header(link_header)
		paging = "last" in links
		repo_url = links['next']

	return repos