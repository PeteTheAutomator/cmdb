import requests
import json


class QueryHandler:
    def __init__(self, repo_url):
        self.repo_url = repo_url

    def get_package_and_version(self, name, version):
        query = json.dumps(
            {
                'rpm_packages.name': name,
                'rpm_packages.version': version,
            }
        )
        params = {
            'where': query
        }
        r = requests.get(self.repo_url, params=params)
        if r.status_code == 200:
            return r._content
        elif r.status_code == 404:
            return False

