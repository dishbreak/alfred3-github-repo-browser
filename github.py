from workflow import web
from collections import defaultdict
import re

PAGE_SIZE = 100

def fetch_page(api_url, token, page_size, reducer=None):
	headers = {"Authorization": "token {}".format(token)}
	params = {"per_page": page_size}
	response = web.get(api_url, params, headers=headers)
	response.raise_for_status()
	repos = response.json()
	if reducer:
		repos = [reducer(x) for x in repos]
	return repos, response.headers['Link']

def parse_header(header):
	rels = [ x.strip() for x in header.split(",")]
	links = defaultdict(lambda: '')
	for rel in rels:
		match = re.match("<(.+)>; rel=\"(.+)\"", rel)
		links[match.group(2)] = match.group(1)
	return links

def make_plucker(fields):
	"""
	Factory method that will create a filtering function.
	The returned function will accept a dict and return only the fields specified
	in the fields parameter.
	"""
	def filter(record):
		result = {}
		for field in fields:
			if field in record:
				result[field] = record[field]
		return result
	return filter

def fetch_repos(api_root, token):
	repo_url = "{}/user/repos".format(api_root)
	paging = True

	reducer = make_plucker(["name", "description", "html_url"])

	repos = []
	while paging:
		page, link_header = fetch_page(repo_url, token, PAGE_SIZE, reducer)
		repos += page
		links = parse_header(link_header)
		paging = "last" in links
		repo_url = links['next']

	return repos