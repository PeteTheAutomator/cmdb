from yum import *
from ansible.module_utils.facts import Facts
import requests
import urlparse
import os


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
        # f = Facts(load_on_init=False)
        # f.get_platform_facts()
        return {'foo': 'bar'}


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

