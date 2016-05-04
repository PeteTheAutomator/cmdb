from yum import *
from ansible.module_utils.facts import Facts
import requests
import urlparse
import os
import json


class YumHandler:
    def __init__(self):
        self.yb = yum.YumBase()
        self.yb.conf.cache = os.geteuid() != 1

    def get(self):
        pl = self.yb.doPackageLists()
        results = []
        if pl.installed:
            for pkg in sorted(pl.installed):
                results.append(
                    {
                        'name': pkg['name'],
                        'version': pkg['version'],
                        'repoid': pkg['repoid'],
                        'packagesize': pkg['packagesize'],
                        'arch': pkg['arch'],
                        'release': pkg['release'],
                    }
                )
        return results


class FacterHandler:
    def __init__(self):
        pass

    def get(self):
        f = Facts(load_on_init=False)
        f.get_platform_facts()
        return f.populate()


class HostMetadata:
    def __init__(self, metadata_url_base='http://169.254.169.254/latest/meta-data/'):
        self.metadata_url_base = metadata_url_base

    def fetch(self, endpoint):
        response = requests.get(urlparse.urljoin(self.metadata_url_base, endpoint), timeout=0.1)
        if response.status_code != 200:
            raise Exception('Unexpected status code {0}'.format(response.status_code))
        return response

    def get(self):
        return self.fetch('instance-id').text


class RepoHandler:
    def __init__(self, config):
        self.config = config

    def post_results(self, results):
        headers = {'Content-Type': 'application/json'}
        r = requests.post(self.config['repo_url'], headers=headers, data=json.dumps(results))
        if r.status_code != 201:
            raise Exception('Unexpected http response ({0}) from {1}'.format(r.status_code, self.config['repo_url']))

    def patch_results(self, results, uuid, etag):
        headers = {'Content-Type': 'application/json', 'If-Match': etag}
        payload = {
            'instance_id': results['instance_id'],
            'rpm_packages': results['rpm_packages'],
            'facts': results['facts'],
        }
        r = requests.patch(self.config['repo_url'] + '/' + uuid + '/', headers=headers, data=json.dumps(payload))
        print 'patched: ({0})'.format(r.status_code)

    def get_doc_id(self, instance_id):
        headers = {'Content-Type': 'application/json'}
        request_url = self.config['repo_url'] + '/' + instance_id + '/'
        r = requests.get(request_url, headers=headers)
        if r.status_code == 200:
            results_dict = json.loads(r._content)
            return results_dict['_id'], results_dict['_etag']
        elif r.status_code == 404:
            return False, False
        else:
            raise Exception('Unexpected http status ({0}) from request: {1}'.format(r.status_code, request_url))

    def post_audit(self, instance_id, results):
        doc_id, etag = self.get_doc_id(instance_id)
        if not doc_id:
            self.post_results(results)
        else:
            self.patch_results(results, uuid=doc_id, etag=etag)