import requests
import json
import re


class QueryHandler:
    def __init__(self, repo_url):
        self.repo_url = repo_url

    def get_with_pagination(self, query):
        query = json.dumps(query)

        params = {
            'where': query
        }

        results_list = []
        r = requests.get(self.repo_url, params=params)

        if r.status_code == 200:
            results = json.loads(r._content)
            results_list.extend(results['_items'])
            if 'last' in results['_links']:
                lastpage = results['_links']['last']['href']
                lastpage_num = re.match('.+=(\d+)$', lastpage).group(1)

                for i in range(2, int(lastpage_num)+1):
                    r = requests.get(self.repo_url + '?page=' + str(i), params=params)
                    results = json.loads(r._content)
                    results_list.extend(results['_items'])
        elif r.status_code == 404:
            return False

        return results_list
