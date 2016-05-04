from cmdb_libs.audit import *
import json


def int_to_str(i):
    return '%08x'%((i+2**24)%2**24)


def doit():
    fh = open('/var/tmp/test.json')
    json_raw = fh.read()
    fh.close()

    test_dict = json.loads(json_raw)

    for i in range(1, 1001):
        instance_id = 'i-' + int_to_str(i)
        test_dict['instance_id'] = instance_id

        config_dict = dict()
        config_dict['repo_url'] = 'http://cmdb-server/audits'
        rh = RepoHandler(config=config_dict)

        rh.post_audit(instance_id, results=test_dict)

doit()
